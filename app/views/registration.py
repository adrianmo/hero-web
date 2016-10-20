import json

from django.shortcuts import render
from formtools.wizard.views import SessionWizardView
import requests

from app.forms import RegistrationInitForm, RegistrationAgreeForm, RegistrationHeroForm, RegistrationPasswordForm
from django.conf import settings
from retrying import retry

FORMS = [
    ("init", RegistrationInitForm),
    ("hero", RegistrationHeroForm),
    ("agree", RegistrationAgreeForm),
    # ("password", RegistrationPasswordForm),
]

TEMPLATES = {
    "init": "registration/init.html",
    "hero": "registration/hero.html",
    "agree": "registration/agree.html",
    # "password": "registration/password.html",
}


class RegistrationWizard(SessionWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, form_dict, **kwargs):
        form_data = {}
        for form in form_list:
            form_data.update(form.cleaned_data)

        token = self.register_user(form_data)

        return render(self.request, 'registration/done.html', {
            'data': form_data,
            'token': token,
        })

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
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
            raise Exception("Could not communicate with Hero API")

        body = r.json()
        return body['token']
