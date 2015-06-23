from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.forms.widgets import CheckboxSelectMultiple
from dor.models import Repository, Journal, Taxonomy, ContentType, Standards, Certification
from dor.widgets import NestedCheckboxSelectMultiple
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
#from RepoDir.settings import TEMPLATES

#ADMIN_TEMPLATES = '{}{}'.format(TEMPLATES[0].get('DIRS')[0], '/admin/')

class RepoAdmin(admin.ModelAdmin):
    model = Repository
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    search_fields = ['name', 'accepted_taxonomy__name',
                     'accepted_content__name']


class JournalAdmin(admin.ModelAdmin):
    model = Journal
    search_fields = ['name', 'repos_endorsed__name'] #, 'repos_endorsed__standards__name']


class TaxAdmin(TreeAdmin):
    form = movenodeform_factory(Taxonomy)
    search_fields = ['name', 'tax_id']


class ContentAdmin(TreeAdmin):
    form = movenodeform_factory(ContentType)
    search_fields = ['name']


class StandardAdmin(admin.ModelAdmin):
    model = Standards
    formfield_overrides = {
        models.ManyToManyField: {'widget': NestedCheckboxSelectMultiple},
    }
    search_fields = ['name']


class CertificationAdmin(TreeAdmin):
    form = movenodeform_factory(Certification)
    search_fields = ['name']


class DORAdminSite(admin.AdminSite):
    site_title = "COPDESS"
    site_header = "COPDESS Administrative Interface"


admin_site = DORAdminSite(name='admin')

admin_site.register(User, UserAdmin)
admin_site.register(Repository, RepoAdmin)
admin_site.register(Journal, JournalAdmin)
admin_site.register(Taxonomy, TaxAdmin)
admin_site.register(ContentType, ContentAdmin)
admin_site.register(Standards, StandardAdmin)
admin_site.register(Certification, CertificationAdmin)
