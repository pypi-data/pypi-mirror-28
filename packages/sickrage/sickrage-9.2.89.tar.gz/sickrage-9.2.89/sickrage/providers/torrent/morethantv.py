# Author: Seamus Wassman
# URL: https://sickrage.ca
#
# This file is part of SickRage.
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import re
from urlparse import urljoin

import requests

import sickrage
from sickrage.core.caches.tv_cache import TVCache
from sickrage.core.exceptions import AuthException
from sickrage.core.helpers import bs4_parser, convert_size, try_int
from sickrage.providers import TorrentProvider


class MoreThanTVProvider(TorrentProvider):
    def __init__(self):
        super(MoreThanTVProvider, self).__init__("MoreThanTV", 'https://www.morethan.tv', True)

        self.urls.update({
            'login': '{base_url}/login.php'.format(**self.urls),
            'detail': '{base_url}/torrents.php'
                      '?id=%s'.format(**self.urls),
            'search': '{base_url}/torrents.php'
                      '?tags_type=1'
                      '&order_by=time'
                      '&order_way=desc'
                      '&action=basic'
                      '&searchsubmit=1'
                      '&searchstr=%s'.format(**self.urls),
            'download': '{base_url}/torrents.php'
                        '?action=download'
                        '&id=%s'.format(**self.urls)
        })

        self._uid = None
        self._hash = None
        self.username = None
        self.password = None

        self.minseed = None
        self.minleech = None

        self.cookies = None

        self.proper_strings = ['PROPER', 'REPACK']

        self.cache = TVCache(self, min_time=10)

    def _check_auth(self):

        if not self.username or not self.password:
            raise AuthException("Your authentication credentials for " + self.name + " are missing, check your config.")

        return True

    def login(self):
        if any(requests.utils.dict_from_cookiejar(self.session.cookies).values()):
            return True

        if self._uid and self._hash:
            requests.utils.add_dict_to_cookiejar(self.session.cookies, self.cookies)
        else:
            login_params = {'username': self.username,
                            'password': self.password,
                            'login': 'Log in',
                            'keeplogged': '1'}

            try:
                self.session.get(self.urls['login'])
                response = self.session.post(self.urls['login'], data=login_params).text
            except Exception:
                sickrage.app.log.warning("Unable to connect to provider".format(self.name))
                return False

            if re.search('logout.php', response):
                return True
            elif re.search('Your username or password was incorrect.', response):
                sickrage.app.log.warning(
                    "Invalid username or password. Check your settings".format(self.name))

    def search(self, search_params, age=0, ep_obj=None):
        results = []

        if not self.login():
            return results

        for mode in search_params.keys():
            sickrage.app.log.debug("Search Mode: %s" % mode)
            for search_string in search_params[mode]:
                if mode != 'RSS':
                    sickrage.app.log.debug("Search string: %s " % search_string)

                searchURL = self.urls['search'] % (search_string.replace('(', '').replace(')', ''))

                # returns top 15 results by default, expandable in user profile to 100
                try:
                    data = self.session.get(searchURL).text
                    results += self.parse(data, mode)
                except Exception:
                    sickrage.app.log.debug("No data returned from provider")

        return results

    def parse(self, data, mode):
        """
        Parse search results from data
        :param data: response data
        :param mode: search mode
        :return: search results
        """

        results = []

        with bs4_parser(data) as html:
            torrent_rows = html.find_all('tr', class_='torrent')
            if len(torrent_rows) < 1:
                sickrage.app.log.debug("Data returned from provider does not contain any torrents")
                return results

            for result in torrent_rows:
                try:
                    # skip if torrent has been nuked due to poor quality
                    if result.find('img', alt='Nuked'):
                        continue

                    download_url = urljoin(self.urls['base_url'] + '/',
                                           result.find('span', title='Download').parent['href'])
                    title = result.find('a', title='View torrent').get_text(strip=True)

                    if not all([title, download_url]):
                        continue

                    seeders = try_int(result('td', class_="number_column")[1].text, 0)
                    leechers = try_int(result('td', class_="number_column")[2].text, 0)

                    size = -1
                    if re.match(r'\d+([,.]\d+)?\s*[KkMmGgTt]?[Bb]',
                                result('td', class_="number_column")[0].text):
                        size = convert_size(result('td', class_="number_column")[0].text.strip(), -1)

                    results += [
                        {'title': title, 'link': download_url, 'size': size, 'seeders': seeders, 'leechers': leechers}
                    ]

                    if mode != 'RSS':
                        sickrage.app.log.debug("Found result: {}".format(title))
                except Exception:
                    sickrage.app.log.error("Failed parsing provider")

        return results