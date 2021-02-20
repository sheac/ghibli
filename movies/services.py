import logging

logger = logging.getLogger(__name__)


class GhibliService:

    def __init__(self, client):
        self.client = client

    def get_film_people(self):
        logger.info("fetching films")
        films = self.client.get_films()
        logger.info("found %s films" % len(films))

        logger.info("fetching people")
        people = self.client.get_people()
        logger.info("found %s people" % len(people))

        film_people = {}
        for film in films:
            film_people[film.id] = {'id': film.id, 'title': film.title, 'people': []}

        for person in people:
            for film_id in person.film_ids:
                film = film_people.get(film_id, None)
                if film is None:
                    continue
                film['people'].append(person.name)

        return list(film_people.values())
