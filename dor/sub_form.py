from django import forms
from treebeard.forms import MoveNodeForm

from dor import models


class RepoSubmissionForm(forms.ModelForm):

    class Meta:
        model = models.Repository
        labels = {
            'name': "Name*",
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
            'date_operational': 'Date Operational*',
            'remarks': 'Remarks*'
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols':80, 'rows':10})
        }

class AnonymousRepoSubmissionForm(forms.ModelForm):

    class Meta:
        model = models.Repository
        labels = {
            'name': "Name*",
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
            'date_operational': 'Date Operational*',
            'remarks': 'Remarks*'
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols':80, 'rows':10})
        }
        exclude = ('allows_embargo_period',)


class TaxSubmissionForm(MoveNodeForm):

    class Meta:
        model = models.Taxonomy
        labels = {
            'name': 'Name*',
            'associated_content': 'Associated Content*',
            'position': 'Position*'
        }
        exclude = ('path', 'depth', 'numchild')

class ContentSubmissionForm(MoveNodeForm):

    class Meta:
        model = models.ContentType
        labels = {
            'name': 'Name*',
            'position': 'Position*'
        }
        exclude = ('lft', 'rgt', 'tree_id', 'depth')

class StandardSubmissionForm(forms.ModelForm):

    class Meta:
        model = models.Standards