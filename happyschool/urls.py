# This file is part of HappySchool.
#
# HappySchool is the legal property of its developers, whose names
# can be found in the AUTHORS file distributed with this source
# distribution.
#
# HappySchool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HappySchool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with HappySchool.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib.auth.views import LoginView, LogoutView, TemplateView

import django_cas_ng.views

from core.utilities import EXCLUDED_APPS

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^core/', include('core.urls')),
    url(r'^annuaire/', include('annuaire.urls'), name='annuaire'),
    url(r'^no_access/', TemplateView.as_view(template_name='core/no_access.html'), name='no_access'),
    url(r'^$', RedirectView.as_view(url='annuaire/', permanent=False)),
]

# Handle SSO with CAS
if "django_cas_ng" in settings.INSTALLED_APPS:
    urlpatterns.append(path("auth", django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'))
    urlpatterns.append(path("logout/", django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'))
    urlpatterns.append(path("login", LoginView.as_view(
        template_name='core/auth.html',
        extra_context={
            'google': 'social_core.backends.google.GoogleOAuth2' in settings.AUTHENTICATION_BACKENDS,
            'microsoft': 'social_core.backends.microsoft.MicrosoftOAuth2' in settings.AUTHENTICATION_BACKENDS,
            'model': 'django.contrib.auth.backends.ModelBackend' in settings.AUTHENTICATION_BACKENDS,
            },
        ), name='auth',))
else:
    urlpatterns.append(url(r'^auth', LoginView.as_view(
        template_name='core/auth.html',
        extra_context={
            'google': 'social_core.backends.google.GoogleOAuth2' in settings.AUTHENTICATION_BACKENDS,
            'microsoft': 'social_core.backends.microsoft.MicrosoftOAuth2' in settings.AUTHENTICATION_BACKENDS,
            'model': 'django.contrib.auth.backends.ModelBackend' in settings.AUTHENTICATION_BACKENDS,
            },
        ), name='auth',))
    urlpatterns.append(url(r'^logout', LogoutView.as_view(next_page='auth'), name='logout'))

for app in settings.INSTALLED_APPS:
    if app in EXCLUDED_APPS:
        continue

    urlpatterns.append(url(r'^%s/' % (app), include('%s.urls' % (app))))

if 'social_django' in settings.INSTALLED_APPS:
    urlpatterns.append(url('', include('social_django.urls', namespace='social')))

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
