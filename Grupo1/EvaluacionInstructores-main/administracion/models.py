from django.db import models
from django import forms
# Create your models here.

class AccessTime(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()