import requests
from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django_countries.fields import LazyTypedChoiceField
from django.db.models.fields import BLANK_CHOICE_DASH
from django_countries import countries
from django.conf import settings
from app import choices


class RegistrationInitForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    country = LazyTypedChoiceField()
    email = forms.EmailField(max_length=100)
    company = forms.CharField(label='Company name (optional)', max_length=100, required=False)
    # position = forms.CharField(label='Position (optional)', max_length=100, required=False)
    phone = forms.CharField(label='Phone (optional)', max_length=100, required=False)
    twitter_handle = forms.CharField(label='Twitter handle (optional)', max_length=100, required=False)

    # github_handle = forms.CharField(label='GitHub username (optional)', max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super(RegistrationInitForm, self).__init__(*args, **kwargs)

        choices = list(countries)
        choices.insert(0, BLANK_CHOICE_DASH[0])
        choices.insert(0, ('', 'Select a country'))
        self.fields['country'].choices = choices


class RegistrationHeroForm(forms.Form):
    hero_name = forms.CharField(max_length=100)
    hero_class = forms.ChoiceField(choices=[(x, x) for x in choices.CLASS_CHOICES])
    hero_title = forms.ChoiceField(choices=[(x, x) for x in choices.TITLE_CHOICES])

    def clean(self):
        cleaned_data = super(RegistrationHeroForm, self).clean()
        try:
            r = requests.get("{endpoint}/hero/{name}".format(
                endpoint=settings.HERO_API,
                name=cleaned_data['hero_name']
            ))

            if r.status_code == 200:
                if 'hero_name' not in self._errors:
                    self._errors['hero_name'] = ErrorList()
                self._errors['hero_name'].append('This Hero name is already taken')
        except Exception as e:
            raise ValidationError(e)
        return cleaned_data


class RegistrationAgreeForm(forms.Form):
    agree = forms.BooleanField(label='I agree with the terms and conditions', required=True)

    def clean(self):
        super(RegistrationAgreeForm, self).clean()
        if not self.cleaned_data['agree']:
            raise forms.ValidationError("You must agree with the terms and conditions.")
        return self.cleaned_data
