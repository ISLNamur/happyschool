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

# Generated by Django 2.2.11 on 2020-04-20 09:54

from django.db import migrations
from django.contrib.auth.models import Permission
from django.db.models import ObjectDoesNotExist


def migrate_access_permission(apps, schema_editor):
    try:
        old_permission = Permission.objects.get(codename="access_infirmerie")
        new_permission = Permission.objects.get(codename="view_passage")
        for g in old_permission.group_set.all():
            g.permissions.add(new_permission)
            g.save()
        for u in old_permission.user_set.all():
            u.user_permissions.add(new_permission)
            u.save()

        # Remove old permission
        old_permission.delete()
    except ObjectDoesNotExist:
        # Old permission never existed, skipping.
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('infirmerie', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_access_permission),
    ]