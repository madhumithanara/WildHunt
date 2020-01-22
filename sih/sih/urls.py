from django.conf.urls import url
from django.contrib import admin
#from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import path, include


urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(),{'template_name': 'logged_out.html'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('user/', include('crophenology.urls')),
]