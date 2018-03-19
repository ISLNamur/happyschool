"""appyschool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from django.contrib.auth.views import LoginView, LogoutView, TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^channels-api/', include('channels_api.urls')),
    url(r'^core/', include('core.urls')),
    url(r'^auth', LoginView.as_view(template_name='core/auth.html'), name='auth'),
    url(r'^logout', LogoutView.as_view(next_page='auth'), name='logout'),
    url(r'^annuaire/', include('annuaire.urls'), name='annuaire'),
    url(r'^no_access/', TemplateView.as_view(template_name='core/no_access.html'), name='no_access'),
]

for app in ['infirmerie', 'appels', 'dossier_eleve', 'absence_prof', 'mail_notification', 'slas', 'mobility_survey',]:
    if app in settings.INSTALLED_APPS:
        urlpatterns.append(url(r'^%s/' % (app), include('%s.urls' % (app))))