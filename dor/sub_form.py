from django import forms
import datetime
from django.core.exceptions import ValidationError

from dor import models


class RepoSubmissionForm(forms.ModelForm):

    class Meta:
        model = models.Repository
