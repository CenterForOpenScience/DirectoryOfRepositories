from django.conf.urls import url, include
from dor import views
from rest_framework.routers import DefaultRouter
#import rest_framework_swagger

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'repos', views.RepositoryViewSet)
router.register(r'journals', views.JournalViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'taxonomy', views.TaxonomyViewSet)
router.register(r'standards', views.StandardsViewSet)
router.register(r'contenttype', views.ContentTypeViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^swag/', include('rest_framework_swagger.urls')),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework'))
]
