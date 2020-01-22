from django.urls import path

from . import views
from django.conf.urls import url

app_name = 'crophenology'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]