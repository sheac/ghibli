from django.test import TestCase

from ..models import Film, Person
from ..services import GhibliService


class MockClient:
    FILMS = [
            Film("abc", "Kickass"),
            Film("def", "The Incredibles"),
            Film("ghi", "The Avengers"),
        ]

    PEOPLE = [
        Person("Rodney Dangerfield", ["abc", "def"]),
        Person("Larry David", ["def"]),
        Person("John Mulaney", ["abc", "def"]),
    ]

    def __init__(self, films, people):
        self.films = films
        self.people = people

    def get_films(self):
        return self.films

    def get_people(self):
        return self.people


class TestServices(TestCase):

    def test_get_film_people_all(self):
        client = MockClient(MockClient.FILMS, MockClient.PEOPLE)
        ghibli_service = GhibliService(client)
        result = ghibli_service.get_film_people()

        for result_film, actual_film in zip(result, MockClient.FILMS):
            self.assertEqual(result_film['title'], actual_film.title)
            people = [
                p.name for p in MockClient.PEOPLE if result_film['id'] in p.film_ids
            ]
            self.assertListEqual(sorted(result_film['people']), sorted(people))

    def test_get_film_people_no_films(self):
        client = MockClient([], MockClient.PEOPLE)

        ghibli_service = GhibliService(client)
        result = ghibli_service.get_film_people()

        self.assertEqual(len(result), 0)

    def test_get_film_people_mismatched_ids(self):
        films = MockClient.FILMS
        for film in films:
            film.id = "not an id that matches any person"
        client = MockClient(films, MockClient.PEOPLE)

        ghibli_service = GhibliService(client)
        result = ghibli_service.get_film_people()

        for result_film, actual_film in zip(result, MockClient.FILMS):
            self.assertEqual(len(result_film['people']), 0)
