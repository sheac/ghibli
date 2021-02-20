import logging

from django.http import JsonResponse
from django.views.decorators.cache import cache_page

from . import config
from .clients import GhibliClient
from .services import GhibliService

logger = logging.getLogger(__name__)

ONE_MINUTE = 60


@cache_page(ONE_MINUTE)
def index(request):
    client = GhibliClient(config.GHIBLI_URL)
    service = GhibliService(client)

    try:
        logger.info("Getting film:people from service")
        film_people = service.get_film_people()
    except:
        logger.exception("Error getting film:people from service")
        return JsonResponse({'success': 'false', 'message': 'internal server error'}, status=500)

    logger.info("Finished serving request")
    return JsonResponse(
        film_people,
        json_dumps_params={'indent': 2},
        safe=False,
    )
