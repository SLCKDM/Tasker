from rest_framework import serializers

from . import models

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    # uuid = serializers.UUIDField(read_only=True)
    # f_name = serializers.CharField(allow_blank=True, max_length=100)
    # l_name = serializers.CharField(allow_blank=True, max_length=100)

    class Meta:
        model = models.Profile
        fields = ['uuid', 'f_name', 'l_name']

    def create(self, validated_data):
        '''
        create and return a new `Profile` instance, given the validated data
        '''
        return models.Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.uuid = validated_data.get('uuid', instance.uuid)
        instance.f_name = validated_data.get('f_name', instance.f_name)
        instance.l_name = validated_data.get('l_name', instance.l_name)
        # instance.group = validated_data.get('group', instance.group)
        instance.save()
        return instance
