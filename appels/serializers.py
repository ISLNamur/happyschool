from rest_framework import serializers

from appels.models import Appel


class AppelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appel
        exclude = ('datetime_encodage',)
        read_only_fields = ('user', 'name',)
