"""URLs for django_co_acls application."""

from django.conf.urls.defaults import *


urlpatterns = patterns('django_co_acls.views',
    url(r'^$', view='index', name='django_co_acls_index'),
)
