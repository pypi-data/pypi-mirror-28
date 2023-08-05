from django.conf.urls import include, url
from django_bugout.views import bugout
app_name = 'django_bugout'

urlpatterns = [
    url(r'^$', bugout),
]
