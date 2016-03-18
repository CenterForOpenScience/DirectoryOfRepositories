from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin
from dor.models import Repository, Journal, Taxonomy, ContentType, Standards, Certification
from dor.widgets import NestedCheckboxSelectMultiple
from django_mptt_admin.admin import DjangoMpttAdmin
from robots.admin import RuleAdmin
from robots.models import Rule, Url
from mptt.models import TreeManyToManyField

class RepoAdmin(admin.ModelAdmin):
    model = Repository
    formfield_overrides = {
        TreeManyToManyField: {'widget': NestedCheckboxSelectMultiple},
    }
    search_fields = ['name', 'accepted_taxonomy__obj_name',
                     'accepted_content__obj_name']

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        old = None
        profile_modified = False
        if 'owner' in form.changed_data:
            old = obj.__class__.objects.get(pk=obj.id)
            if obj.owner:
                if not obj.owner.is_staff:
                    profile_modified = True
                    try:
                        obj.owner.userprofile.maintains_obj = True
                    except AttributeError:
                        new_profile = UserProfile(user=obj.owner, user_type='Repository Representative', maintains_obj=True)
                        obj.owner.userprofile = new_profile

        obj.save()

        if profile_modified:
            obj.owner.userprofile.save()

        if old and old.owner and not old.owner.is_staff and not obj.__class__.objects.filter(owner=old.owner):
            try:
                old.owner.userprofile.maintains_obj = False
                old.owner.userprofile.save()
            except AttributeError:
                pass


class CustomUserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        new_profile = None
        if not obj.is_staff:
            try:
                obj.userprofile
            except AttributeError:
                new_profile = UserProfile(user=obj, user_type='Repository Representative')
                obj.userprofile = new_profile
        obj.save()

        if new_profile:
            import ipdb; ipdb.set_trace()
            new_profile.save()


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    search_fields = ['user', 'maintains_obj', 'user_type']

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
admin_site.register(Rule, RuleAdmin)
admin_site.register(Url)
admin_site.register(Site, SiteAdmin)
admin_site.register(Repository, RepoAdmin)
admin_site.register(Journal, JournalAdmin)
admin_site.register(Taxonomy, TaxAdmin)
admin_site.register(ContentType, ContentAdmin)
admin_site.register(Standards, StandardAdmin)
admin_site.register(Certification, CertificationAdmin)
