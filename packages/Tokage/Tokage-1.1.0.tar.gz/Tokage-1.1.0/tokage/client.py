import asyncio
import json
from html.parser import HTMLParser
from urllib.parse import parse_qs

import aiohttp
from lxml import etree

from .anime import Anime
from .character import Character
from .errors import *  # noqa
from .manga import Manga
from .person import Person
from .utils import parse_id
from .partial import *  # noqa

BASE_URL = 'https://api.jikan.me/'
ANIME_URL = BASE_URL + 'anime/'
MANGA_URL = BASE_URL + 'manga/'
PERSON_URL = BASE_URL + 'person/'
CHARACTER_URL = BASE_URL + 'character/'
SEARCH_URL = BASE_URL + 'search/'


class Client:
    """Client connection to the MAL API.
    This class is used to interact with the API.

    :param Optional[aiohttp.ClientSession] session:
        The session to use for aiohttp requests.
        Defaults to creating a new one.

    Attributes
    ----------
    session : aiohttp.ClientSession

        The session used for aiohttp requests.

    """
    def __init__(self, session=None, *, loop=None):
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.session = aiohttp.ClientSession(loop=self.loop) if session is None else session
        self.html_parser = HTMLParser()

    async def cleanup(self):
        await self.session.close()

    async def _json(self, resp, encoding=None):
        """Read, decodes and unescapes a JSON `aiohttp.ClientResponse` object."""
        def unescape_json(json_data):
            if isinstance(json_data, str):
                return self.html_parser.unescape(json_data)
            if isinstance(json_data, list):
                return [unescape_json(i) for i in json_data]
            if isinstance(json_data, dict):
                return {
                    unescape_json(k): unescape_json(v)
                    for k, v in json_data.items()
                }
            return json_data

        if resp._content is None:
            await resp.read()

        stripped = resp._content.strip()
        if not stripped:
            return None

        if encoding is None:
            encoding = resp._get_encoding()

        json_resp = json.loads(stripped.decode(encoding))

        return unescape_json(json_resp)

    async def request(self, url):
        async with self.session.get(url) as resp:
            return await self._json(resp)

    async def get_anime(self, target_id):
        """Retrieves an :class:`Anime` object from an ID

        Raises a :class:`AnimeNotFound` Error if an Anime was not found corresponding to the ID.
        """
        resp = await self.request(ANIME_URL + str(target_id))
        if resp is None:
            raise AnimeNotFound("Anime with the given ID was not found")
        result = Anime(target_id, resp)
        return result

    async def get_manga(self, target_id):
        """Retrieves a :class:`Manga` object from an ID

        Raises a :class:`MangaNotFound` Error if a Manga was not found corresponding to the ID.
        """
        resp = await self.request(MANGA_URL + str(target_id))
        if resp is None:
            raise MangaNotFound("Manga with the given ID was not found")
        result = Manga(target_id, resp)
        return result

    async def get_character(self, target_id):
        """Retrieves a :class:`Character` object from an ID

        Raises a :class:`CharacterNotFound` Error if a Character was not found corresponding to the ID.
        """
        resp = await self.request(CHARACTER_URL + str(target_id))
        if resp is None:
            raise CharacterNotFound("Character with the given ID was not found")
        result = Character(target_id, resp)
        return result

    async def get_person(self, target_id):
        """Retrieves a :class:`Person` object from an ID

        Raises a :class:`PersonNotFound` Error if a Person was not found corresponding to the ID.
        """
        resp = await self.request(PERSON_URL + str(target_id))
        if resp is None:
            raise PersonNotFound("Person with the given ID was not found")
        result = Person(target_id, resp)
        return result

    async def search_anime(self, query):
        """Search for :class:`PartialAnime` by query.
        
        Returns a list of results.
        """
        resp = await self.request(SEARCH_URL + "anime/" + query)
        if resp is None or not resp['result']:
            raise AnimeNotFound("Anime `{}` could not be found".format(query))
        return [PartialAnime(a['title'], a['id'], a['url']) for a in resp['result']]
    
    async def search_manga(self, query):
        """Search for :class:`PartialManga` by query.
        
        Returns a list of results.
        """
        resp = await self.request(SEARCH_URL + "manga/" + query)
        if resp is None or not resp['result']:
            raise MangaNotFound("Manga `{}` could not be found".format(query))
        return [PartialManga(m['title'], m['id'], m['url']) for m in resp['result']]
    
    async def search_character(self, query):
        """Search for :class:`PartialCharacter` by query.
        
        Returns a list of results.
        """
        resp = await self.request(SEARCH_URL + "character/" + query)
        if resp is None or not resp['result']:
            raise CharacterNotFound("Character `{}` could not be found".format(query))
        return [PartialCharacter.from_search(c) for c in resp['result']]
    
    async def search_person(self, query):
        """Search for :class:`PartialPerson` by query.
        
        Returns a list of results.
        """
        resp = await self.request(SEARCH_URL + "person/" + query)
        if resp is None or not resp['result']:
            raise PersonNotFound("Person `{}` could not be found".format(query))
        return [PartialPerson(p['name'], p['id'], p['url']) for p in resp['result']]

    async def search_id(self, type_, query):
        """Parse a google query and return the ID.

        Raises a :class:`TokageNotFound` Error if an ID was not found.
        """
        query = "site:myanimelist.net/{}/ {}".format(type_, query)
        params = {
            'q': query,
            'safe': 'on'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)'
        }

        url = 'https://www.google.com/search'
        async with self.session.get(url, params=params, headers=headers) as resp:
            if resp.status != 200:
                raise RuntimeError('Google somehow failed to respond.')

            root = etree.fromstring(await resp.text(), etree.HTMLParser())
            nodes = root.findall(".//div[@class='g']")
            for node in nodes:
                url_node = node.find('.//h3/a')
                if url_node is None:
                    continue

                url = url_node.attrib['href']
                if not url.startswith('/url?'):
                    continue

                url = parse_qs(url[5:])['q'][0]
                id = parse_id(url)
                if id is None:
                    raise TokageNotFound("An ID corresponding to the given query was not found")
                return id
