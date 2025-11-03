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
import datetime

from django.utils import timezone
from django.conf import settings
from django.http import HttpRequest

from core.models import MenuEntryModel

EXCLUDED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "channels",
    "crispy_forms",
    "social_django",
    "webpack_loader",
    "proeco",
    "django_cas_ng",
    "debug_toolbar",
    "django_vite_plugin",
    "hijack",
    "hijack.contrib.admin",
]


def get_scholar_year() -> int:
    """Get current scholar year. The scholar year starts from core settings."""

    from core.views import get_core_settings as get_settings

    current_date = timezone.now()
    year = current_date.year
    month = current_date.month
    day = current_date.day

    core_settings = get_settings()
    if month < core_settings.month_scholar_year_start:
        return year - 1
    elif (
        month == core_settings.month_scholar_year_start
        and day < core_settings.day_scholar_year_start
    ):
        return year - 1

    return year


def get_current_scholar_year_interval() -> tuple:
    """Get the starting and ending date of the current scholar
    year."""
    from core.views import get_core_settings as get_settings

    scholar_year = get_scholar_year()
    core_settings = get_settings()

    start_date = datetime.date(
        scholar_year, core_settings.month_scholar_year_start, core_settings.day_scholar_year_start
    )
    return (start_date, start_date + datetime.timedelta(days=364))


def in_scholar_year(date) -> bool:
    """Determines whether a given date falls within the current
    scholar year."""
    from core.views import get_core_settings as get_settings

    current_year = get_scholar_year()
    if date.year < current_year:
        return False

    core_settings = get_settings()

    if date.year == current_year:
        if date.month > core_settings.month_scholar_year_start:
            return True
        if (
            date.month == core_settings.month_scholar_year_start
            and date.day >= core_settings.day_scholar_year_start
        ):
            return True

    if date.year == current_year + 1:
        if date.month < core_settings.month_scholar_year_start:
            return True
        if (
            date.month == core_settings.month_scholar_year_start
            and date.day < core_settings.day_scholar_year_start
        ):
            return True

    return False


def get_menu(request: HttpRequest, active_app: str = "") -> dict:
    apps = []
    for app in settings.INSTALLED_APPS:
        if app in EXCLUDED_APPS:
            continue
        if app == "core":
            continue
        module = importlib.import_module("%s.views" % app)
        try:
            get_menu_entry = getattr(module, "get_menu_entry")
            menu_entry = get_menu_entry(active_app, request)
            if menu_entry:
                apps.append(menu_entry)
        except AttributeError:
            pass

    for entry in MenuEntryModel.objects.filter(forced_order=None):
        apps.append(
            {
                "app": entry.id,
                "display": entry.display,
                "url": entry.link,
                "active": False,
                "new_tab": True,
            }
        )

    for entry in MenuEntryModel.objects.filter(forced_order__isnull=False):
        apps.insert(
            entry.forced_order,
            {
                "app": entry.id,
                "display": entry.display,
                "url": entry.link,
                "active": False,
                "new_tab": True,
            },
        )

    full_name = request.user.get_full_name() if not request.user.is_anonymous else "anonymous"
    menu = {"full_name": full_name, "apps": apps}
    menu["admin_settings"] = request.user.has_perm("core.add_coresettingsmodel")

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


def extract_day_of_week(day_of_week: str) -> list:
    if not day_of_week:
        return []

    seq_days = day_of_week.strip().split(",")

    # Ensure range or single day are well formatted (!= from x or x-y).
    if [seq for seq in seq_days if len(seq.strip()) != 1 and len(seq.strip()) != 3]:
        raise ValueError

    days = [int(day.strip()) for day in seq_days if len(day.strip()) == 1]
    ranges = [seq.strip() for seq in seq_days if len(seq.strip()) == 3]
    for r in ranges:
        if r[1] != "-":
            raise ValueError
        if int(r[0]) > int(r[2]):
            raise ValueError
        days += list(range(int(r[0]), int(r[2]) + 1))
    days = list(set(days))
    days.sort()
    return days
