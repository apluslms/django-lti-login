"""
Url conf for example app
"""
from django.urls import include, path, re_path
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
    path('login/', auth_login,
        {'template_name': 'login.html'},
        name='login'),
    path('logout/', auth_logout,
        {'next_page': '/'},
        name='logout'),
]

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('auth/', include('django_lti_login.urls')), # XXX: for django-lti-login
    path('auth/', include(auth_urlpatterns)),

    path('', frontpage, name='frontpage'),
]
