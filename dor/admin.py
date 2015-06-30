from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from dor.models import Repository, Journal, Taxonomy, ContentType, Standards, Certification
from dor.widgets import NestedCheckboxSelectMultiple
from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.models import TreeManyToManyField

class RepoAdmin(admin.ModelAdmin):
    model = Repository
    #formfield_overrides = {
    #    TreeManyToManyField: {'widget': NestedCheckboxSelectMultiple},
    #}
    search_fields = ['name', 'accepted_taxonomy__obj_name',
                     'accepted_content__obj_name']


class JournalAdmin(admin.ModelAdmin):
    model = Journal
    search_fields = ['name', 'repos_endorsed__name']  # , 'repos_endorsed__standards__name']


class TaxAdmin(DjangoMpttAdmin):
    search_fields = ['obj_name', 'tax_id']


class ContentAdmin(DjangoMpttAdmin):
    search_fields = ['obj_name']

class StandardAdmin(admin.ModelAdmin):
    model = Standards
    #formfield_overrides = {
    #    models.ManyToManyField: {'widget': NestedCheckboxSelectMultiple},
    #}
    search_fields = ['name']


class CertificationAdmin(DjangoMpttAdmin):
    #form = movenodeform_factory(Certification)
    search_fields = ['obj_name']


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
