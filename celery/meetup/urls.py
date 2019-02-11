"""
meetup URL Configuration
"""

from django.conf.urls import url
from meetup import views

urlpatterns = [
    url(r'^longRunningTask/?$', views.task_view, name='task_view'),
]
