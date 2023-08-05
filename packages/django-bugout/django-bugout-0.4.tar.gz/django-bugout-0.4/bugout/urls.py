from django.conf.urls import include, url
from bugout.views import debug_wizard
app_name = 'django_bugout'

urlpatterns = [
    url(r'^$', debug_wizard),
]
