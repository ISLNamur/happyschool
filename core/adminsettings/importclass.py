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

import csv
from typing import Union, TextIO
from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from core.models import StudentModel, TeachingModel, ClasseModel, AdditionalStudentInfo


class ImportBase:
    """Base class to import students and responsible"""

    def __init__(self, teaching: TeachingModel) -> None:
        self.teaching = teaching

    def _sync(self, iterable) -> None:
        pass

    """Get value from an entry."""
    def get_value(self, entry: object, column: str) -> Union[int, str, date, None]:
        return self.format_value(entry[column], column)

    """Handle different entry format."""
    def format_value(self, value: Union[int, str], column: str) -> Union[int, date, str, None]:
        pass

    """Print progress"""
    def print_log(self, log: str) -> None:
        print(log)


class ImportStudent(ImportBase):
    """Base class for importing students."""

    additional_columns = [
        "gender", "scholar_year", "previous_class",
        "orientation", "street", "postal_code",
        "locality", "student_phone", "student_mobile",
        "student_email", "resp_last_name", "resp_first_name",
        "resp_phone", "resp_mobile", "resp_email",
        "father_last_name", "father_first_name",
        "father_job", "father_phone", "father_mobile",
        "father_email",
        "mother_last_name", "mother_first_name",
        "mother_job","mother_phone", "mother_mobile",
        "mother_email",
        "doctor", "doctor_phone", "mutual",
        "mutual_number", "medical_information",
        "birth_date", "username", "password",
    ]

    def format_value(self, value: Union[int, str], column: str) -> Union[int, str, date, None]:
        if type(value) == str and len(value) == 0:
            return None
        if column == "year":
            if len(value) == 1:
                return int(value)
            if len(value) > 1:
                if value[0].isdigit():
                    return int(value[0])
                # Try second character.
                else:
                    return int(value[1])
        if column == "classe_letter":
            return value.lower()
        if column == "birth_date":
            return date(year=int(value[:4]),
                 month=int(value[4:6]),
                 day=int(value[6:]))

        return value

    def _sync(self, iterable) -> None:
        if not self.teaching:
            self.print_log("teaching is missing, aborting.")
            return
        processed = 0
        student_synced = set()
        self.print_log("Importing students…")
        for entry in iterable:
            # First check mandatory field.
            matricule = int(self.get_value(entry, "matricule"))
            if not matricule:
                self.print_log("No matricule found, skipping student.")
                continue
            first_name = self.get_value(entry, "first_name")
            if not first_name:
                self.print_log("No first name found, skipping student.")
                continue
            last_name = self.get_value(entry, "last_name")
            if not last_name:
                self.print_log("No last name found, skipping student.")
                continue
            year = self.get_value(entry, "year")
            if not year:
                self.print_log("No year found, skipping student (%s %s)."
                               % (last_name, first_name))
                continue
            classe_letter = self.get_value(entry, "classe_letter")
            if not classe_letter:
                self.print_log("No classe letter found, skipping student (%s %s)."
                               % (last_name, first_name))
                continue
            try:
                student = StudentModel.objects.get(matricule=matricule)
                student.inactive_from = None
            except ObjectDoesNotExist:
                student = StudentModel(matricule=matricule)

            student.first_name = first_name
            student.last_name = last_name
            student.teaching = self.teaching

            # Check if student's classe already exists.
            try:
                classe = ClasseModel.objects.get(year=year,
                                                 letter=classe_letter,
                                                 teaching=self.teaching)
            except ObjectDoesNotExist:
                classe = ClasseModel(year=year,
                                     letter=classe_letter,
                                     teaching=self.teaching)
                classe.save()

            student.classe = classe
            student.save()

            student_synced.add(student.matricule)

            # Print progress.
            processed += 1
            if processed % 50 == 0:
                self.print_log(processed)

            # Additional info.
            try:
                info = student.additionalstudentinfo
            except ObjectDoesNotExist:
                info = AdditionalStudentInfo(student=student)
            for c in self.additional_columns:
                val = self.get_value(entry, c)
                if val:
                    setattr(info, c, val)
            info.save()

        # Set inactives.
        self.print_log("Set inactive students…")
        all_students = StudentModel.objects.filter(teaching=self.teaching)
        for s in all_students:
            if s.matricule not in student_synced:
                s.inactive_from = timezone.make_aware(timezone.datetime.now())
                s.classe = None
                s.save()

        self.print_log("Import done.")


class ImportStudentCSV(ImportStudent):
    def __init__(self, teaching: TeachingModel, column_map: dict=None,
                 column_index: dict=None) -> None:
        super().__init__(teaching)
        self.column_map = column_map
        if not column_index:
            self.column_to_index = {j: i for i, j in
                                    enumerate(["matricule", "last_name", "first_name",
                                               "year", "classe_letter"])}
        else:
            self.column_to_index = column_index

    def sync(self, text: TextIO, ignore_first_line: bool=False,
             has_header: bool=False) -> None:
        # First detect dialect.
        dialect = csv.Sniffer().sniff(text.readline())
        # Return to start.
        text.seek(0)

        reader = csv.reader(text, dialect)
        if ignore_first_line:
            next(reader, None)
        # Map column to row index with first line.
        if has_header:
            header = next(reader, None)
            if self.column_map:
                self.column_to_index = {self.column_map[j]: i for i, j in
                                        enumerate(header)}
            else:
                self.column_to_index = {j: i for i, j in
                                        enumerate(header)}

        super()._sync(reader)

    def get_value(self, entry: list, column: str) -> Union[int, str, date, None]:
        try:
            return self.format_value(entry[self.column_to_index[column]], column)
        except KeyError:
            return None
