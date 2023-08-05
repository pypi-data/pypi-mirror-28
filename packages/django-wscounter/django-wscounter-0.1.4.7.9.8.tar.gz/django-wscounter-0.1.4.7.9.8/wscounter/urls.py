"""
Urls for wscounter views
"""

from django.conf.urls import url

from wscounter import views

urlpatterns = [
    url(r'^$', views.WSCounterAPIView.as_view(), name='counter_api'),
]
