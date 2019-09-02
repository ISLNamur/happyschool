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

from pathlib import Path
import shutil
import importlib

from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User


EXCLUDED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'channels',
    'crispy_forms',
    'social_django',
    'webpack_loader',
]


def get_scholar_year() -> int:
    """Get current scholar year. The scholar year starts the 8th of August."""
    current_date = timezone.now()
    year = current_date.year
    month = current_date.month
    day = current_date.day

    if month < 8:
        return year - 1
    elif month == 8 and day < 20:
        return year - 1
    else:
        return year


def in_scholar_year(date) -> bool:
    current_year = get_scholar_year()
    if date.year < current_year:
        return False

    if date.month >= 9 and date.year == current_year:
        return True

    if date.month < 9 and date.year == current_year + 1:
        return True

    return False


def get_menu(user: User, active_app: str=None) -> dict:
    apps = []
    for app in settings.INSTALLED_APPS:
        if app in EXCLUDED_APPS:
            continue
        if app == "core":
            continue
        try:
            module = importlib.import_module("%s.views" % app)
            get_menu_entry = getattr(module, 'get_menu_entry')
            menu_entry = get_menu_entry(active_app, user)
            if menu_entry:
                apps.append(menu_entry)
        except:
            pass

    menu = {"full_name": user.get_full_name(), "apps": apps}
    menu['admin_settings'] = user.has_perm('core.add_coresettingsmodel')

    return menu


def check_student_photo(student, copy=True) -> bool:
    photos_dir = Path(settings.BASE_DIR).joinpath("static/photos/")
    student_photo = photos_dir.joinpath(str(student.matricule) + ".jpg")
    if not student_photo.is_file():
        if copy:
            # Copy unknown.jpg to [matricule].jpg
            shutil.copy(str(photos_dir.joinpath("unknown.jpg")), str(student_photo))
        return False
    return True
