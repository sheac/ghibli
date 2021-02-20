import json
import logging
from urllib.parse import urljoin
from urllib.request import urlopen

from .models import Film, Person

logger = logging.getLogger(__name__)


class GhibliClient:

    def __init__(self, url):
        self.url = url

    def films_url(self):
        return urljoin(self.url, "films/")

    def people_url(self):
        return urljoin(self.url, "people/")

    def get_films(self):
        logger.info("fetching films")
        resp = urlopen(self.films_url())
        logger.info("response code: %s" % resp.getcode())
        films_json = json.loads(resp.read().decode("utf-8"))
        return list(map(self.json_to_film, films_json))

    def get_people(self):
        logger.info("fetching people")
        resp = urlopen(self.people_url())
        logger.info("response code: %s" % resp.getcode())
        people_json = json.loads(resp.read().decode('utf-8'))
        return list(map(self.json_to_person, people_json))

    def json_to_film(self, film_json):
        return Film(film_json['id'], film_json['title'])

    def json_to_person(self, person_json):
        return Person(
            person_json['name'],
            map(lambda f: f.replace(self.films_url(), ""), person_json['films'])
        )
