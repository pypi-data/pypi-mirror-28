"""Module for searching torrents on LinuxTracker."""
import logging
from typing import List, Tuple

import bs4

from mariner import searchengine, torrent

Magnet = str
Name = str
Url = str


class LinuxTracker(searchengine.TrackerPlugin):
    """Represents LinuxTracker search engine."""

    log = logging.getLogger(__name__)

    search_url = 'http://linuxtracker.org/index.php?page=torrents&search='

    def _parse(self, raw: str) -> List[Tuple[Name, Magnet, Url]]:
        """Parse result page.

        Args:
          raw: Raw HTML results page to parse.

        Returns:
            List of torrent names with magnet links.
        """
        soup = bs4.BeautifulSoup(raw, 'lxml')
        content = soup.find_all('table', {'class': 'lista', 'width': '100%'})
        for torrent_ in content[4]:
            try:
                name = str(torrent_.font.a.string)
                tracker = self.__class__.__name__

                links = torrent_.find_all('td', {'align': 'right'})[0]
                magnet = links.find_all('a')[0]['href']
                stub = links.find_all('a')[1]['href']
                url = f'http://linuxtracker.org/{stub}'

                raw_seeds = torrent_.find_all(
                    'tr')[2].get_text().split(' ')[-2]
                seeds = self._parse_number(raw_seeds)

                yield torrent.Torrent(name, tracker, torrent=url, magnet=magnet, seeds=seeds)
            except AttributeError:
                pass
