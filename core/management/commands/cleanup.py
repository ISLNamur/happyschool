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

from dateutil.relativedelta import relativedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import TeachingModel, ClasseModel, CourseModel, StudentModel


class Command(BaseCommand):
    help = 'Clean up database. Clear empty classes and courses, and remove students older than 6 years.'

    def add_arguments(self, parser):
        parser.add_argument(
            "-i",
            '--implementation',
            help="Specify teaching, default all teachings."
        )

        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Just show objects that will be removed; don't actually remove them."
        )

        parser.add_argument(
            "-o",
            "--older-than",
            default=6,
            help="The number of year of inactivity before students will be deleted."
        )

        parser.add_argument(
            "--only-classes",
            action="store_true",
            help="Clean only classes."
        )

        parser.add_argument(
            "--only-courses",
            action="store_true",
            help="Clean only courses."
        )

        parser.add_argument(
            "--only-students",
            action="store_true",
            help="Clean only students."
        )

    def clean_classes(self, options, teachings):
        classes = ClasseModel.objects.filter(
            studentmodel__isnull=True,
            teaching__in=teachings
        )

        print("Removing empty classes :")
        for c in classes:
            print(c)
        if not options["dry_run"]:
            classes.delete()

    def clean_courses(self, options, teachings):
        courses = CourseModel.objects.filter(
            givencoursemodel__studentmodel__isnull=True,
            givencoursemodel__responsiblemodel__isnull=True,
            teaching__in=teachings
        )

        print("Removing empty courses :")
        for c in courses:
            print(c)
        if not options["dry_run"]:
            courses.delete()

    def clean_students(self, options, teachings):
        students = StudentModel.objects.filter(
            classe__isnull=True,
            courses__isnull=True,
            inactive_from__lte=timezone.now() - relativedelta(years=options["older_than"]),
            teaching__in=teachings
        )

        print(f"Removing old students (at least {options['older_than']} years of inactivity):")
        for s in students:
            print(s)
        if not options["dry_run"]:
            students.delete()

    def handle(self, *args, **options):
        teaching_filter_field = {"name": options["implementation"]} if options["implementation"] else {}
        teachings = TeachingModel.objects.filter(**teaching_filter_field)

        if not options["only_courses"] and not options["only_students"]:
            self.clean_classes(options, teachings)

        if not options["only_classes"] and not options["only_students"]:
            self.clean_courses(options, teachings)

        if not options["only_courses"] and not options["only_classes"]:
            self.clean_students(options, teachings)

        return
