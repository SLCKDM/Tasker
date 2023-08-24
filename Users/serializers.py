from rest_framework import serializers

from . import models

class GroupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)

    class Meta:
        model = models.Group
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField(allow_blank=True, max_length=100)
    is_active = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    groups = GroupSerializer(many=True)

    class Meta:
        model = models.User
        fields = [
            'id',
            'username',
            'email',
            'is_active',
            'is_superuser',
            'groups'
        ]


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    url = serializers.HyperlinkedIdentityField(
        view_name='api:profiles-detail',
        lookup_field='uuid',
    )
    class Meta:
        model = models.Profile
        fields = [
            'url',
            'uuid',
            'f_name',
            'l_name',
            'user',
        ]

    def create(self, validated_data: dict) -> models.Profile:
        '''
        create and return a new `Profile` instance, given the validated data
        '''
        return models.Profile.objects.create(**validated_data)

    def update(self, instance: models.Profile, validated_data: dict) -> models.Profile:
        instance.uuid = validated_data.get('uuid', instance.uuid)
        instance.f_name = validated_data.get('f_name', instance.f_name)
        instance.l_name = validated_data.get('l_name', instance.l_name)
        # instance.group = validated_data.get('group', instance.group)
        instance.save()
        return instance
