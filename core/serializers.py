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

from core.models import *


class ResponsibleSensitiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsibleModel
        fields = ('pk', 'last_name', 'first_name', 'is_secretary', 'email', 'email_school', 'teaching', 'user', 'password')
        depth = 1


class ResponsibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsibleModel
        fields = ('pk', 'matricule', 'last_name', 'first_name', 'is_secretary', 'email_school',
                  'teaching', 'classe', 'tenure', 'display')
        depth = 1


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModel
        fields = ('matricule', 'first_name', 'last_name', 'display', 'classe', 'teaching', 'user',)
        depth = 1


class StudentGeneralInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalStudentInfo
        fields = ('student', 'gender', 'scholar_year', 'previous_classe',
                  'orientation', 'birth_date', 'street', 'postal_code',
                  'locality', 'username', 'password')


class StudentContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalStudentInfo
        fields = ('student',
                  'student_phone', 'student_mobile', 'student_email',
                  'resp_last_name', 'resp_first_name', 'resp_phone', 'resp_mobile', 'resp_email',
                  'mother_last_name', 'mother_first_name', 'mother_phone', 'mother_mobile', 'mother_email',
                  'father_last_name', 'father_first_name', 'father_phone', 'father_mobile', 'father_email',
                  )


class StudentMedicalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalStudentInfo
        fields = ('student', 'doctor', 'doctor_phone', 'mutual', 'mutual_number', 'medical_information')


class ClasseSerializer(serializers.ModelSerializer):
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
        fields = '__all__'


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
            return ClasseModel.objects.filter(year=data[0], teaching__display_name=data.split(" — ")[1]).first()
        else:
            return ClasseModel.objects.filter(year=data[0]).first()


class YearSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.show_teaching = kwargs.pop("show_teaching", True)
        super().__init__(*args, **kwargs)
        self.fields["display"] = YearField(source='*', show_teaching=self.show_teaching)

    display = YearField(source='*', show_teaching=True)

    class Meta:
        model = ClasseModel
        fields = ('display',)


class TeachingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachingModel
        fields = '__all__'


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailModel
        fields = '__all__'
