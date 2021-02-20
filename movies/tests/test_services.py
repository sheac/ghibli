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

    def get_films(self):
        return MockClient.FILMS

    def get_people(self):
        return MockClient.PEOPLE


class TestServices(TestCase):

    def test_get_film_people(self):
        ghibli_service = GhibliService(MockClient())
        result = ghibli_service.get_film_people()

        for result_film, actual_film in zip(result, MockClient.FILMS):
            self.assertEqual(result_film['title'], actual_film.title)
            people = [
                p.name for p in MockClient.PEOPLE if result_film['id'] in p.film_ids
            ]
            self.assertListEqual(sorted(result_film['people']), sorted(people))
