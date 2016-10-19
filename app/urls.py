from django.conf.urls import url
from django.views.generic import TemplateView

from app.views import index, hero, registration, tutorial

urlpatterns = [
    url(r'^$', index.index, name='index'),
    url(r'^registration/$', registration.RegistrationWizard.as_view(registration.FORMS), name='registration'),
    url(r'^tutorial/$', tutorial.TutorialView.as_view(), name='tutorial'),

    # Hero
    url(r'^hero/$', hero.info, name='hero_info'),
    url(r'^hero/events/$', hero.info, name='hero_events'),
    url(r'^hero/players/$', hero.info, name='hero_player_list'),
    url(r'^hero/players/(?P<player_id>[\w-]+)/$', hero.info, name='hero_player_details'),
    url(r'^hero/map/$', hero.info, name='hero_map'),

    # Temp
    url(r'^done/$', TemplateView.as_view(template_name='registration/done.html')),
]
