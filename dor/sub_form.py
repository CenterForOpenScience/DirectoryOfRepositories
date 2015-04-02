from django import forms
import datetime
from django.core.exceptions import ValidationError

from dor import models


class RepoSubmissionForm(forms.ModelForm):

    class Meta:
        model = models.Repository
        labels = {
            'alt_names': 'Alternate Names',
            'url': 'Url*',
            'persistent_url': 'Persistent Url*',
            'accepted_taxonomy': 'Accepted Taxonomy*',
            'accepted_content': 'Accepted Data-Types*',
            'standards': 'Standards*',
            'hosting_institution': 'Hosting Institution',
            'institution_country': 'Institution Country',
            'owner': 'Owner*',
            'metadataStandardName': 'Metadata Standard Name*',
            'metadataStandardURL': 'Metadata Standard URL*',
            'metadataRemarks': 'Metadata Remarks',
            'size': 'Size*',
            'date_operational': 'Date Operational*'
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols':80, 'rows':10})
        }


class TaxSubmissionForm(forms.ModelForm):

    class Meta:
        model = models.Taxonomy

class ContentSubmissionForm(forms.ModelForm):

    class Meta:
        model = models.ContentType

class StandardSubmissionForm(forms.ModelForm):

    class Meta:
        model = models.Standards