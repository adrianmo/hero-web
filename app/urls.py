from django.conf.urls import url
from django.views.generic import TemplateView

from app.views import index, hero, registration, tutorial, status

urlpatterns = [
    url(r'^$', index.index, name='index'),
    url(r'^registration/$', registration.RegistrationWizard.as_view(registration.FORMS), name='registration'),
    url(r'^tutorial/$', tutorial.TutorialView.as_view(), name='tutorial'),

    # Hero
    url(r'^game/$', hero.info, name='hero_info'),
    url(r'^game/events/$', hero.event_list, name='hero_events'),
    url(r'^game/players/$', hero.player_list, name='hero_player_list'),
    url(r'^game/players/(?P<player_name>[\w-]+)/$', hero.player_details, name='hero_player_details'),
    url(r'^game/map/$', hero.map, name='hero_map'),

    # Status
    url(r'^status/$', status.status, name='status'),
]
