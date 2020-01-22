from django.urls import path

from . import views
from django.conf.urls import url

app_name = 'crophenology'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload_data/',views.upload_data,name='upload_data'),
    path('charts/',views.upload_data,name='chart'),
]