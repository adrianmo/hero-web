import requests
from django.shortcuts import render
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def info(request):
    return render(request, 'hero/info.html', {})


def events(request):
    error = None
    events = []
    try:
        r = requests.get("{endpoint}/events".format(endpoint=settings.HERO_API))

        if r.status_code < 200 or r.status_code >= 300:
            error = "Could not obtain events"
        else:
            data = r.json()
            events = data['events']
    except requests.ConnectionError as e:
        logger.error(e)
        error = "Could not connect to Hero API"
    except Exception as e:
        logger.error(e)
        error = str(e)

    return render(request, 'hero/events.html', {'events': events, 'error': error})


def player_list(request):
    error = None
    players = []
    try:
        r = requests.get("{endpoint}/hero".format(endpoint=settings.HERO_API))

        if r.status_code < 200 or r.status_code >= 300:
            error = "Could not obtain player list"
        else:
            data = r.json()
            players = data['heroes']
    except requests.ConnectionError as e:
        logger.error(e)
        error = "Could not connect to Hero API"
    except Exception as e:
        logger.error(e)
        error = str(e)

    return render(request, 'hero/player_list.html', {'players': players, 'error': error})


def player_details(request, player_name):
    try:
        r = requests.get("{endpoint}/hero/{name}".format(endpoint=settings.HERO_API, name=player_name))
        if r.status_code < 200 or r.status_code >= 300:
            error = "Could not obtain player info"
            return render(request, 'hero/player_details.html', {'error': error})
        player = r.json()

        r = requests.get("{endpoint}/hero/{name}/events".format(endpoint=settings.HERO_API, name=player_name))
        if r.status_code < 200 or r.status_code >= 300:
            error = "Could not obtain player events"
            return render(request, 'hero/player_details.html', {'error': error})
        data = r.json()
        player_events = data['events']

        return render(request, 'hero/player_details.html', {'player': player, 'events': player_events})
    except requests.ConnectionError as e:
        logger.error(e)
        error = "Could not connect to Hero API"
    except Exception as e:
        logger.error(e)
        error = str(e)

    return render(request, 'hero/player_details.html', {'error': error})


def map(request):
    error = None
    players = []
    try:
        r = requests.get("{endpoint}/hero".format(endpoint=settings.HERO_API))

        if r.status_code < 200 or r.status_code >= 300:
            error = "Could not obtain player list"
        else:
            data = r.json()
            players = data['heroes']

    except requests.ConnectionError as e:
        logger.error(e)
        error = "Could not connect to Hero API"
    except Exception as e:
        logger.error(e)
        error = str(e)

    return render(request, 'hero/map.html', {'players': players, 'error': error})
