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
        form_data = {}
        for form in form_list:
            form_data.update(form.cleaned_data)

        try:
            form_data['token'] = self.register_user(form_data)
            self.send_email(form_data)
        except requests.ConnectionError as e:
            logger.error(e)
            error = "Could not connect to Hero API"
        except Exception as e:
            logger.error(e)
            error = str(e)

        return render(self.request, 'registration/done.html', {
            'data': form_data,
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

Please, take note of your username and Hero token as you need them to complete the tutorial and participate in the contest.

You can log in with the following credentials.

Email: {email}
Token: {token}
Neutrino URL: {neutrino_url}
Horizon URL: {horizon_url}

The VxRack Neutrino team.
        """.format(name=data['first_name'], email=data['email'], token=data['token'],
                   neutrino_url=settings.NEUTRINO_URL, horizon_url=settings.HORIZON_URL)
        email = EmailMessage('Welcome to VxRack Neutrino Heroes tutorial', body, to=[data['email']])
        if email.send() != 1:
            raise Exception('Could not send email')
        return
