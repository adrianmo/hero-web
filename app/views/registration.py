import json

from django.core.mail import EmailMessage
from django.shortcuts import render
from formtools.wizard.views import SessionWizardView
import requests

from app.forms import RegistrationInitForm, RegistrationAgreeForm, RegistrationHeroForm
from django.conf import settings
from retrying import retry

import logging

logger = logging.getLogger(__name__)

FORMS = [
    ("init", RegistrationInitForm),
    ("hero", RegistrationHeroForm),
    ("agree", RegistrationAgreeForm),
]

TEMPLATES = {
    "init": "registration/init.html",
    "hero": "registration/hero.html",
    "agree": "registration/agree.html",
}


class RegistrationWizard(SessionWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, form_dict, **kwargs):
        error = None
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)

        data['neutrino_account'] = 'default'
        data['neutrino_username'] = 'user'
        data['neutrino_url'] = settings.NEUTRINO_URL

        try:
            data['token'] = self.register_user(data)
            self.send_email(data)
        except requests.ConnectionError as e:
            logger.error(e)
            error = "Could not connect to Hero API"
        except Exception as e:
            logger.error(e)
            error = str(e)

        return render(self.request, 'registration/done.html', {
            'data': data,
            'error': error,
        })

    @retry(stop_max_attempt_number=3, wait_fixed=1000)
    def register_user(self, data):
        r = requests.post("{endpoint}/hero".format(endpoint=settings.HERO_API), json={
            'firstName': data['first_name'],
            'lastName': data['last_name'],
            'email': data['email'],
            'heroName': data['hero_name'],
            'heroClass': data['hero_class'],
            'heroTitle': data['hero_title'],
            'twitter': data['twitter_handle'],
        }, headers={'X-Auth-Token': settings.HERO_ADMIN_TOKEN})

        if r.status_code < 200 or r.status_code >= 300:
            raise Exception("Error: %s" % (r.content,))

        body = r.json()['token']
        return body

    @retry(stop_max_attempt_number=3, wait_fixed=1000)
    def send_email(self, data):
        body = """
Hello {name},

Thanks for participating in the VxRack Neutrino Heroes tutorial!

You can start the tutorial in the following site.

http://vxrackneutrinoheroes.com/tutorial

Your credentials to access the VxRack Neutrino are the following.

- Neutrino account: {neutrino_account}
- Neutrino username: {neutrino_username}
- Neutrino URL: {neutrino_url}
- Horizon URL: {neutrino_url}/horizon/

Please, also take note of your Hero name and token as you need them to complete the tutorial and participate in the contest.

- Hero name: {hero_name}
- Token: {token}

The VxRack Neutrino team.
        """.format(neutrino_account=data['neutrino_account'],
                   neutrino_username=data['neutrino_username'],
                   neutrino_url=data['neutrino_url'],
                   name=data['first_name'],
                   hero_name=data['hero_name'],
                   token=data['token'])
        email = EmailMessage('Welcome to VxRack Neutrino Heroes tutorial', body, to=[data['email']])
        if email.send() != 1:
            raise Exception('Could not send email')
        return
