from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from dor.models import Taxonomy

class MyAdmin(TreeAdmin):
    form = movenodeform_factory(Taxonomy)

admin.site.register(Taxonomy, MyAdmin)
