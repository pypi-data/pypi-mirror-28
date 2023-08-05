from django.conf.urls import include, url
from django_bugout.views import debug_wizard
app_name = 'django_bugout'

urlpatterns = [
    url(r'^$', debug_wizard.as_view()),
]
