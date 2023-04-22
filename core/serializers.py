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

from rest_framework import serializers

from django.contrib.auth.models import User, Group

from core.models import *


class CourseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label="ID", read_only=False)

    class Meta:
        model = CourseModel
        fields = "__all__"


class GivenCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = GivenCourseModel
        fields = ["id", "course", "group", "display", "classes", "teachers"]
        depth = 1


class GivenCourseFlatSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label="ID", read_only=False)

    class Meta:
        model = GivenCourseModel
        fields = "__all__"


class ResponsibleSensitiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsibleModel
        fields = (
            "pk",
            "last_name",
            "first_name",
            "is_secretary",
            "email",
            "email_school",
            "teaching",
            "user",
            "password",
        )
        depth = 1


class ResponsibleSerializer(serializers.ModelSerializer):
    courses = GivenCourseSerializer(read_only=True, many=True)

    class Meta:
        model = ResponsibleModel
        fields = (
            "pk",
            "matricule",
            "last_name",
            "first_name",
            "is_secretary",
            "email_school",
            "teaching",
            "classe",
            "tenure",
            "display",
            "courses",
        )
        depth = 2


class ResponsibleRemoteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label="ID", read_only=False)

    class Meta:
        model = ResponsibleModel
        fields = (
            "id",
            "matricule",
            "last_name",
            "first_name",
            "is_teacher",
            "is_educator",
            "is_secretary",
            "teaching",
            "classe",
            "tenure",
            "email_school",
            "courses",
            "user",
        )


class StudentSerializer(serializers.ModelSerializer):
    courses = GivenCourseSerializer(read_only=True, many=True)
    group = serializers.CharField(source="additionalstudentinfo.group")

    class Meta:
        model = StudentModel
        fields = (
            "matricule",
            "first_name",
            "last_name",
            "display",
            "classe",
            "teaching",
            "user",
            "courses",
            "group",
        )
        depth = 2

    def __init__(self, *args, **kwargs):
        no_course = kwargs.pop("no_course", True)

        super(StudentSerializer, self).__init__(*args, **kwargs)

        if no_course:
            self.fields.pop("courses")


class StudentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModel
        fields = (
            "matricule",
            "first_name",
            "last_name",
            "classe",
            "teaching",
            "inactive_from",
            "courses",
        )


class StudentSensitiveInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalStudentInfo
        fields = (
            "student",
            "birth_date",
            "street",
            "postal_code",
            "locality",
            "father_job",
            "mother_job",
        )


class StudentGeneralInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalStudentInfo
        fields = (
            "student",
            "gender",
            "group",
            "scholar_year",
            "previous_classe",
            "orientation",
            "username",
            "password",
        )


class StudentContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalStudentInfo
        fields = (
            "student",
            "student_phone",
            "student_mobile",
            "student_email",
            "resp_last_name",
            "resp_first_name",
            "resp_phone",
            "resp_mobile",
            "resp_email",
            "mother_last_name",
            "mother_first_name",
            "mother_phone",
            "mother_mobile",
            "mother_email",
            "father_last_name",
            "father_first_name",
            "father_phone",
            "father_mobile",
            "father_email",
        )


class StudentMedicalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalStudentInfo
        fields = (
            "student",
            "doctor",
            "doctor_phone",
            "mutual",
            "mutual_number",
            "medical_information",
        )


class ClasseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label="ID", read_only=False)

    # Enable showing/hiding teaching
    def __init__(self, *args, **kwargs):
        show_teaching = kwargs.pop("show_teaching", True)
        if not show_teaching:
            self.source_type = "compact_str"
        else:
            self.source_type = "__str__"
        super().__init__(*args, **kwargs)
        self.fields["display"] = serializers.CharField(source=self.source_type, read_only=True)

    class Meta:
        model = ClasseModel
        fields = "__all__"


class YearField(serializers.Field):
    def __init__(self, *args, **kwargs):
        self.show_teaching = kwargs.pop("show_teaching", True)
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        out = str(value.year)
        if value.year == 1:
            out += "ère année"
        else:
            out += "ème année"

        if self.show_teaching:
            out += " – " + value.teaching.display_name
        return out

    def to_internal_value(self, data):
        if self.show_teaching:
            return ClasseModel.objects.filter(
                year=data[0], teaching__display_name=data.split(" — ")[1]
            ).first()
        else:
            return ClasseModel.objects.filter(year=data[0]).first()


class YearSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.show_teaching = kwargs.pop("show_teaching", True)
        super().__init__(*args, **kwargs)
        self.fields["display"] = YearField(source="*", show_teaching=self.show_teaching)

    display = YearField(source="*", show_teaching=True)

    class Meta:
        model = ClasseModel
        fields = ("display",)


class TeachingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label="ID", read_only=False, required=False)

    class Meta:
        model = TeachingModel
        fields = "__all__"


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailModel
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label="ID", read_only=False)

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
        )


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label="ID", read_only=False)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "last_name",
            "first_name",
            "email",
            "groups",
        )


class CourseScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseScheduleModel
        fields = (
            "id",
            "given_course",
            "period",
            "day_of_week",
            "related_classes",
            "related_responsibles",
            "place",
        )
        read_only_fields = (
            "related_classes",
            "related_responsibles",
        )


class PeriodCoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodCoreModel
        fields = "__all__"
