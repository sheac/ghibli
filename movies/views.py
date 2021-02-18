from django.http import JsonResponse

from . import config
from .clients import GhibliClient
from .services import GhibliService


def index(request):
    client = GhibliClient(config.GHIBLI_URL)
    service = GhibliService(client)
    film_people = service.get_film_people()

    return JsonResponse(
        film_people,
        json_dumps_params={'indent': 2},
        safe=False,
    )
