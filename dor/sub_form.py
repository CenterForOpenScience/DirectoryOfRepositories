from django import forms
from mptt.forms import MoveNodeForm

from dor import models


class JournalSubmissionForm(forms.ModelForm):

    class Meta:
        model = models.Journal
        fields = "__all__"
        labels = {
            'name': "Name*",
            'url': 'Url*',
            'repos_endorsed': "Endorsed Repositories"
        }
        widgets = {
            'repos_endorsed': forms.CheckboxSelectMultiple(),
        }
        exclude = ('owner', 'is_visible',)

    def save(self, user=None, commit=True):
        inst = super(JournalSubmissionForm, self).save(commit=False)
        inst.owner = user
        if commit:
            inst.save()
            self.save_m2m()
        return inst

class RepoSubmissionForm(forms.ModelForm):

    class Meta:
        model = models.Repository
        fields = "__all__"
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
            'metadataInformationURL': 'Metadata Information URL*',
            'metadataRemarks': 'Metadata Remarks',
            'size': 'Size*',
            'date_operational': 'Date Operational*',
            'remarks': 'Remarks*',
            'db_certifications': 'Database Certificaions*',
        }
        widgets = {
            'accepted_content': forms.CheckboxSelectMultiple(),
            'db_certifications': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'metadataRemarks': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'remarks': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }
        exclude = ('owner',)

    def save(self, user=None, commit=True):
        inst = super(RepoSubmissionForm, self).save(commit=False)
        inst.owner = user
        if commit:
            inst.save()
            self.save_m2m()
        return inst

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
            'metadataInformationURL': 'Metadata Information URL*',
            'metadataRemarks': 'Metadata Remarks',
            'size': 'Size*',
            'date_operational': 'Date Operational*',
            'remarks': 'Remarks*',
            'db_certifications': 'Database Certificaions*',
        }
        widgets = {
            'accepted_content': forms.CheckboxSelectMultiple(),
            'db_certifications': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'metadataRemarks': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'remarks': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }
        exclude = ('embargoed',)


class TaxSubmissionForm(MoveNodeForm):

    class Meta:
        model = models.Taxonomy
        labels = {
            'name': 'Name*',
            'associated_content': 'Associated Content*',
            'position': 'Position*'
        }
        exclude = ('lft', 'rght', 'tree_id', 'level')


class ContentSubmissionForm(MoveNodeForm):

    class Meta:
        model = models.ContentType
        labels = {
            'name': 'Name*',
            'position': 'Position*'
        }
        exclude = ('lft', 'rght', 'tree_id', 'level')


class CertificationSubmissionForm(MoveNodeForm):

    class Meta:
        model = models.Certification
        labels = {
            'name': 'Name*',
            'position': 'Position*'
        }
        exclude = ('lft', 'rght', 'tree_id', 'level')


class StandardSubmissionForm(forms.ModelForm):

    class Meta:
        model = models.Standards
        fields = "__all__"
