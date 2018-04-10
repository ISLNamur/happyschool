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

from django.utils import timezone


def get_scolar_year():
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


def in_scolar_year(date):
    current_year = get_scolar_year()
    if date.year < current_year:
        return False

    if date.month >= 9 and date.year == current_year:
        return True

    if date.month < 9 and date.year == current_year + 1:
        return True

    return False