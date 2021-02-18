class GhibliService:

    def __init__(self, client):
        self.client = client

    def get_film_people(self):
        films = self.client.get_films()
        people = self.client.get_people()

        film_people = {}
        for film in films:
            film_people[film.id] = {'title': film.title, 'people': []}

        for person in people:
            for film_id in person.film_ids:
                film = film_people.get(film_id, None)
                if film is None:
                    continue
                film['people'].append(person.name)

        return list(film_people.values())
