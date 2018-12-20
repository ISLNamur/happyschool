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
from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib.auth.views import LoginView, LogoutView, TemplateView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^core/', include('core.urls')),
    url(r'^auth', LoginView.as_view(template_name='core/auth.html'), name='auth'),
    url(r'^logout', LogoutView.as_view(next_page='auth'), name='logout'),
    url(r'^annuaire/', include('annuaire.urls'), name='annuaire'),
    url(r'^no_access/', TemplateView.as_view(template_name='core/no_access.html'), name='no_access'),
    url(r'^$', RedirectView.as_view(url='annuaire/', permanent=False)),
]

for app in ['infirmerie', 'appels', 'dossier_eleve', 'absence_prof', 'mail_notification', 'slas', 'mobility_survey',
            'mail_answer', 'schedule_change', 'student_absence']:
    if app in settings.INSTALLED_APPS:
        urlpatterns.append(url(r'^%s/' % (app), include('%s.urls' % (app))))

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
