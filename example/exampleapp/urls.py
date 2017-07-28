"""
Url conf for example app
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth

from .views import frontpage

if hasattr(auth, 'LoginView'):
    auth_login = auth.LoginView.as_view()
    auth_logout = auth.LogoutView.as_view()
else:
    auth_login = auth.login
    auth_logout = auth.logout

auth_urlpatterns = [
    url(r'^login/$', auth_login,
        {'template_name': 'login.html'},
        name='login'),
    url(r'^logout/$', auth_logout,
        {'next_page': '/'},
        name='logout'),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^auth/', include('django_lti_login.urls')), # XXX: for django-lti-login
    url(r'^auth/', include(auth_urlpatterns)),

    url(r'^$', frontpage, name='frontpage'),
]
