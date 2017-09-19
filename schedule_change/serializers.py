from rest_framework import serializers, fields
from .models import ScheduleChange, ScheduleChangeSettings


class FlatArrayField(fields.Field):
    def to_internal_value(self, data):
        return ";".join(data)

    def to_representation(self, value):
        return ", ".join(value.split(";"))


class ScheduleChangeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField()
    datetime_encodage = serializers.ReadOnlyField()
    classes = FlatArrayField()
    teachers = FlatArrayField()
    time_start = serializers.TimeField(allow_null=True)
    time_end = serializers.TimeField(allow_null=True)

    class Meta:
        model = ScheduleChange
        fields = ('id', 'date_start', 'date_end', 'time_start',
                  'time_end', 'activity', 'classes', 'teachers', 'place', 'comment', 'user', 'datetime_encodage')


class ScheduleChangeSettingsSerializer(serializers.ModelSerializer):
    teaching = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = ScheduleChangeSettings
        fields = '__all__'
