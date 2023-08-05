"""
Urls for wscounter views
"""

from django.conf.urls import patterns, url

from wscounter import views

urlpatterns = patterns(
    '',
    url(r'^$', views.WSCounterAPIView.as_view(), name='counter_api'),
)
