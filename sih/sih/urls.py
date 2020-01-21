from django.conf.urls import url
from django.contrib import admin
#from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), {'next_page': '/'}, name='logout'),
    url(r'^admin/', admin.site.urls),
]