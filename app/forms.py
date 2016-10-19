from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm
from django_countries.fields import LazyTypedChoiceField
from django.db.models.fields import BLANK_CHOICE_DASH
from django_countries import countries


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
    hero_class = forms.CharField(max_length=100)
    hero_title = forms.CharField(max_length=100)


class RegistrationAgreeForm(forms.Form):
    agree = forms.BooleanField(label='I agree with the terms and conditions', required=True)

    def clean(self):
        super(RegistrationAgreeForm, self).clean()
        if not self.cleaned_data['agree']:
            raise forms.ValidationError("You must agree with the terms and conditions.")
        return self.cleaned_data


class RegistrationPasswordForm(forms.Form):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    def clean(self):
        super(RegistrationPasswordForm, self).clean()
        password = self.cleaned_data.get('password')
        password_validation.validate_password(password)
        return self.cleaned_data
