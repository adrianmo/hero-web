import requests
from django.shortcuts import render
from app.models import NeutrinoAccount
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def status(request):
    data = {}

    data['hero_api'] = ''

    try:
        r = requests.get("{endpoint}/hero".format(endpoint=settings.HERO_API))

        if r.status_code < 200 or r.status_code >= 300:
            data['hero_api'] = 'ERROR: {}'.format(r.content)
        else:
            data['hero_api'] = 'OK'
    except Exception as e:
        logger.error(e)
        data['hero_api'] = 'ERROR: {}'.format(str(e))

    try:
        data['available_accounts'] = len(NeutrinoAccount.objects.filter(used=False))
        data['database'] = 'OK'
    except Exception as e:
        logger.error(e)
        data['available_accounts'] = 'N/A'
        data['database'] = 'ERROR: {}'.format(str(e))

    return render(request, 'status.html', data)


