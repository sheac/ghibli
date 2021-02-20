from urllib.request import urlopen
from urllib.parse import urljoin
import json

from .models import Film, Person


class GhibliClient:

    def __init__(self, url):
        self.url = url

    def films_url(self):
        return urljoin(self.url, "films/")

    def people_url(self):
        return urljoin(self.url, "people/")

    def get_films(self):
        resp = urlopen(self.films_url()).read()
        films_json = json.loads(resp.decode("utf-8"))
        return map(self.json_to_film, films_json)

    def get_people(self):
        resp = urlopen(self.people_url()).read()
        people_json = json.loads(resp.decode('utf-8'))
        return map(self.json_to_person, people_json)

    def json_to_film(self, film_json):
        return Film(film_json['id'], film_json['title'])

    def json_to_person(self, person_json):
        return Person(
            person_json['name'],
            map(lambda f: f.replace(self.films_url(), ""), person_json['films'])
        )
