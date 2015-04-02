from django.contrib import admin
from django.db import models
from dor.models import Repository, Journal, Taxonomy
from dor.widgets import NestedCheckboxSelectMultiple
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


class RepoAdmin(admin.ModelAdmin):
    model = Repository
    formfield_overrides = {
        models.ManyToManyField: {'widget': NestedCheckboxSelectMultiple},
    }
    search_fields = ['name', 'accepted_taxonomy__name',
                     'accepted_content__name']


class JournalAdmin(admin.ModelAdmin):
    model = Journal
    search_fields = ['name', 'repos_endorsed__name', 'repos_endorsed__standards__name']


class TaxAdmin(TreeAdmin):
    form = movenodeform_factory(Taxonomy)
    search_fields = ['name', 'tax_id']


admin.site.register(Repository, RepoAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(Taxonomy, TaxAdmin)