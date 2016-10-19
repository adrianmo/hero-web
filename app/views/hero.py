from django.shortcuts import render


def info(request):
    return render(request, 'hero/info.html', {})


def events(request):
    return render(request, 'hero/events.html', {})


def player_list(request):
    return render(request, 'hero/player_list.html', {})


def player_details(request):
    return render(request, 'hero/player_details.html', {})


def map(request):
    return render(request, 'hero/map.html', {})
