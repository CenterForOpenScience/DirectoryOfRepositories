from django.conf.urls import url, include, patterns
from django.contrib import admin
from dor import views
from dor import models
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
import rest_framework_swagger
from dor import api
from dor.admin import admin_site

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'repos', views.RepositoryViewSet)
router.register(r'journals', views.JournalViewSet)
#router.register(r'users', views.UserViewSet)
router.register(r'taxonomy', views.TaxonomyViewSet)
#router.register(r'standards', views.StandardsViewSet)
router.register(r'contenttype', views.ContentTypeViewSet)
router.register(r'certifications', views.CertificationViewSet)

# Dictionary of models to be used in one template
model_list = {
    'queryset': models.Taxonomy.objects.all(),
    'template_object_name': 'taxonomy',
    'extra_context': {
        'standards': models.Standards.objects.all(),
        'content-types': models.ContentType.objects.all()
    }
}

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = (
    url(r'^admin/', include(admin_site.urls)),
    url(r'^swag/', include('rest_framework_swagger.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', 'dor.views.index'),
    url(r'^login/$', 'dor.views.login'),
    url(r'^auth/$', 'dor.views.auth_view'),
    url(r'^logout/$', 'dor.views.logout'),
    url(r'^register/$', 'dor.views.register'),
    url(r'^invalid/$', 'dor.views.invalid_login'),
    url(r'^ajax_search/', 'dor.views.repositorySearch'),
    url(r'^ajax_filter/', 'dor.views.repositoryFilter'),
    url(r'^search/', 'dor.views.repository_list'),
    url(r'^submit/(?P<title>[-\w]+)/$', 'dor.views.submit'),
    url(r'^manage/$', 'dor.views.manage'),
    url(r'^manage/(?P<title>[-\w]+)/$', 'dor.views.manage_group'),
    url(r'^manage/(?P<title>[-\w]+)/(?P<pk>[0-9]+)/$', 'dor.views.manage_form'),
    url(r'^endorse_repo/$', 'dor.views.endorse'),
    url(r'^approve_embargo_repo/$', 'dor.views.approve_embargo'),
    url(r'^delete_item/$', 'dor.views.delete_item'),
    url(r'^add_data_type/$', 'dor.views.add_data_type'),
    url(r'^add_cert/$', 'dor.views.add_cert'),
    url(r'^add_tax/$', 'dor.views.add_tax'),
    url(r'^robots\.txt$', include('robots.urls')),
)
