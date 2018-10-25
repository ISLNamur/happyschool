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

from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User


def get_scholar_year():
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


def in_scholar_year(date):
    current_year = get_scholar_year()
    if date.year < current_year:
        return False

    if date.month >= 9 and date.year == current_year:
        return True

    if date.month < 9 and date.year == current_year + 1:
        return True

    return False


def get_menu(user: User, active_app: str=None) -> list:
    apps = [{
        "app": "annuaire",
        "display": "Annuaire",
        "url": "/annuaire/",
        "active": active_app == "annuaire"
    }]

    if "infirmerie" in settings.INSTALLED_APPS and user.has_perm('infirmerie.access_infirmerie'):
        apps.append({
            "app": "infirmerie",
            "display": "Infirmerie",
            "url": "/infirmerie",
            "active": active_app == "infirmerie"
        })

    if "appels" in settings.INSTALLED_APPS and user.has_perm('appels.access_appel'):
        apps.append({
            "app": "appels",
            "display": "Appels",
            "url": "/appels/",
            "active": active_app == "appels"
        })

    if "absence_prof" in settings.INSTALLED_APPS and user.has_perm('absence_prof.access_absences'):
        apps.append({
            "app": "absence_prof",
            "display": "Absences Profs",
            "url": "/absence_prof/",
            "active": active_app == "absence_prof"
        })

    if "dossier_eleve" in settings.INSTALLED_APPS and user.has_perm('dossier_eleve.access_dossier_eleve'):
        apps.append({
            "app": "dossier_eleve",
            "display": "Dossier élèves",
            "url": "/dossier_eleve/",
            "active": active_app == "dossier_eleve"
        })

    if "mail_notification" in settings.INSTALLED_APPS and user.has_perm('mail_notification.access_mail_notification'):
        apps.append({
            "app": "mail_notification",
            "display": "Email",
            "url": "/mail_notification",
            "active": active_app == "mail_notification"
        })

    if "schedule_change" in settings.INSTALLED_APPS and user.has_perm('schedule_change.access_schedule_change'):
        apps.append({
            "app": "schedule_change",
            "display": "Changement Horaire",
            "url": "/schedule_change",
            "active": active_app == "schedule_change"
        })

    menu = {"full_name": user.get_full_name(), "apps": apps}

    return menu


def check_student_photo(student, copy=True):
    photos_dir = Path(settings.BASE_DIR).joinpath("static/photos/")
    student_photo = photos_dir.joinpath(str(student.matricule) + ".jpg")
    if not student_photo.is_file():
        if copy:
            # Copy unknown.jpg to [matricule].jpg
            shutil.copy(photos_dir.joinpath("unknown.jpg"), student_photo)
        return False
    return True
