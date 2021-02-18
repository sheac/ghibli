from urllib.request import urlopen
from urllib.parse import urljoin
import json

from .models import Film, Person


class GhibliClient:

    def __init__(self, url):
        self.url = url

    def get_films(self):
        resp = urlopen(urljoin(self.url, "films")).read()
        films_json = json.loads(resp.decode("utf-8"))
        return map(lambda f: Film(f['id'], f['title']), films_json)

    def get_people(self):
        resp = urlopen(urljoin(self.url, "people")).read()
        people_json = json.loads(resp.decode('utf-8'))

        def film_id_from_url(film_url):
            return film_url.replace(urljoin(self.url, "films/"), "")

        def json_to_person(json_person):
            return Person(
                json_person['name'],
                map(film_id_from_url, json_person['films'])
            )

        return map(json_to_person, people_json)
