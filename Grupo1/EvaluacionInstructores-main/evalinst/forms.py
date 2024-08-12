from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from .models import *
from django.forms import ModelForm


class LogInForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class preguntasForm(ModelForm):
    class Meta:
        model = Testings
        fields = '__all__'
