import json

from django.shortcuts import render
from formtools.wizard.views import SessionWizardView

from app.forms import RegistrationInitForm, RegistrationAgreeForm, RegistrationHeroForm, RegistrationPasswordForm
# from app.tasks import register_user

FORMS = [
    ("init", RegistrationInitForm),
    ("hero", RegistrationHeroForm),
    ("agree", RegistrationAgreeForm),
    ("password", RegistrationPasswordForm),
]

TEMPLATES = {
    "init": "registration/init.html",
    "hero": "registration/hero.html",
    "agree": "registration/agree.html",
    "password": "registration/password.html",
}


class RegistrationWizard(SessionWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, form_dict, **kwargs):
        form_data = {}
        for form in form_list:
            form_data.update(form.cleaned_data)
        # register_user.delay(form_data)
        return render(self.request, 'registration/done.html', {
            'form_data': form_data,
        })
