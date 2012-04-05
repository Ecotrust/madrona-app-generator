from django import forms
from django.forms import ModelForm
from appgen.models import AppConfig, BaseKml, UserFeature

class AppConfigForm(ModelForm):
    class Meta:
        model = AppConfig

class BaseKmlForm(ModelForm):
    class Meta:
        model = BaseKml

class UserFeatureForm(ModelForm):
    class Meta:
        model = UserFeature

