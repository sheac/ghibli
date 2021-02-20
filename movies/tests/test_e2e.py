from django.test import TestCase, Client
import httpretty

from ..config import GHIBLI_URL
from ..clients import GhibliClient

class TestE2E(TestCase):

    @httpretty.activate
    def test_movies_smoke(self):

        throwaway_client = GhibliClient(GHIBLI_URL)

        httpretty.register_uri(
            httpretty.GET,
            throwaway_client.films_url(),
            body="""[
                {"id": "abc", "title": "Godzilla"},
                {"id": "def", "title": "King Kong"}
            ]"""
        )

        httpretty.register_uri(
            httpretty.GET,
            throwaway_client.people_url(),
            body="""[
                {"name": "Matt Damon", "films": ["%sabc"]}
            ]""" % throwaway_client.films_url()
        )

        client = Client()
        response = client.get("/movies/")

        self.assertEqual(response.status_code, 200)
        response_content = response.content.decode("utf-8")
        self.assertIn("Godzilla", response_content)
        self.assertIn("King Kong", response_content)
        self.assertIn("Matt Damon", response_content)

    @httpretty.activate
    def test_movies_remote_failure(self):

        throwaway_client = GhibliClient(GHIBLI_URL)

        httpretty.register_uri(
            httpretty.GET,
            throwaway_client.films_url(),
            status=404,
        )

        client = Client()
        response = client.get("/movies/")

        self.assertEqual(response.status_code, 500)
        response_content = response.content.decode("utf-8")
        self.assertIn("internal server error", response_content)

    @httpretty.activate
    def test_movies_malformed_response(self):

        throwaway_client = GhibliClient(GHIBLI_URL)

        httpretty.register_uri(
            httpretty.GET,
            throwaway_client.films_url(),
            body="""[ {"id": "a"id{{"""
        )

        client = Client()
        response = client.get("/movies/")

        self.assertEqual(response.status_code, 500)
        response_content = response.content.decode("utf-8")
        self.assertIn("internal server error", response_content)


