from django.http import JsonResponse

from . import config
from .clients import GhibliClient
from .services import GhibliService


def index(request):
    client = GhibliClient(config.GHIBLI_URL)
    service = GhibliService(client)

    try:
        film_people = service.get_film_people()
    except:
        return JsonResponse({'success': 'false', 'message': 'internal server error'}, status=500)

    return JsonResponse(
        film_people,
        json_dumps_params={'indent': 2},
        safe=False,
    )
