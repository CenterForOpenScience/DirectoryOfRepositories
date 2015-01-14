from django.contrib import admin
from django.db import models
from dor.models import Repository, Journal
from dor.widgets import NestedCheckboxSelectMultiple


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

admin.site.register(Repository, RepoAdmin)
admin.site.register(Journal, JournalAdmin)
