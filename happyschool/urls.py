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

from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib.auth.views import LoginView, LogoutView, TemplateView

from core.utilities import EXCLUDED_APPS

urlpatterns = [
    path("admin/", admin.site.urls),
    path("core/", include("core.urls")),
    path("annuaire/", include("annuaire.urls"), name="annuaire"),
    path("no_access/", TemplateView.as_view(template_name="core/no_access.html"), name="no_access"),
    path("", RedirectView.as_view(url="annuaire/", permanent=False)),
]

# Handle SSO with CAS
if "django_cas_ng" in settings.INSTALLED_APPS:
    import django_cas_ng.views

    urlpatterns.append(path("auth/", django_cas_ng.views.LoginView.as_view(), name="cas_ng_login"))
    urlpatterns.append(
        path("logout/", django_cas_ng.views.LogoutView.as_view(), name="cas_ng_logout")
    )
    urlpatterns.append(
        path(
            "login/",
            LoginView.as_view(
                template_name="core/auth.html",
                extra_context={
                    "google": "social_core.backends.google.GoogleOAuth2"
                    in settings.AUTHENTICATION_BACKENDS,
                    "microsoft": "social_core.backends.microsoft.MicrosoftOAuth2"
                    in settings.AUTHENTICATION_BACKENDS,
                    "model": "django.contrib.auth.backends.ModelBackend"
                    in settings.AUTHENTICATION_BACKENDS,
                },
            ),
            name="auth",
        )
    )
else:
    urlpatterns.append(
        path(
            "auth/",
            LoginView.as_view(
                template_name="core/auth.html",
                extra_context={
                    "google": "social_core.backends.google.GoogleOAuth2"
                    in settings.AUTHENTICATION_BACKENDS,
                    "microsoft": "social_core.backends.microsoft.MicrosoftOAuth2"
                    in settings.AUTHENTICATION_BACKENDS,
                    "model": "django.contrib.auth.backends.ModelBackend"
                    in settings.AUTHENTICATION_BACKENDS,
                },
            ),
            name="auth",
        )
    )
    urlpatterns.append(path("logout/", LogoutView.as_view(next_page="auth"), name="logout"))

for app in settings.INSTALLED_APPS:
    if app in EXCLUDED_APPS:
        continue

    urlpatterns.append(path("%s/" % (app), include("%s.urls" % (app))))

if "social_django" in settings.INSTALLED_APPS:
    urlpatterns.append(path("", include("social_django.urls", namespace="social")))

if "debug_toolbar" in settings.INSTALLED_APPS:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
