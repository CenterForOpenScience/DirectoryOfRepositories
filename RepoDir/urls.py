from django.contrib import admin
from django.conf.urls import include, url

admin.autodiscover()

urlpatterns = [
    url(r'^', include('dor.urls')),
    url(r'^admin/', include(admin.site.urls))
]
