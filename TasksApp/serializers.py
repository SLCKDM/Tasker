from cgitb import lookup
from rest_framework import serializers
from rest_framework import exceptions
from rest_framework import status
from . import models
import Users.models


class MetadataExtensionSerializer(serializers.BaseSerializer):
    detail_view = None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        fields = getattr(self, 'fields')
        if not self.detail_view:
            raise AttributeError(f'`detail_view` name not provided in {type(self)}')
        metadata = {
            'url': fields['url'].get_url(instance, self.detail_view, request=self.context['request'], format=None),
            'object_type': instance.__class__.__name__,
            'mediatype': 'application/json',
        }
        data['metadata'] = metadata
        data.pop('url')
        for key in metadata:
            if key in data:
                data.pop(key)
        return data


class CheckListItemSerializer(MetadataExtensionSerializer, serializers.HyperlinkedModelSerializer):
    detail_view = 'api:checkitems-detail'

    url = serializers.HyperlinkedIdentityField(
        view_name="api:checkitems-detail",
        lookup_field="uuid",
    )
    check_list = serializers.HyperlinkedRelatedField(
        queryset = models.CheckList.objects.all(),
        view_name = "api:checklists-detail",
        lookup_field = "uuid"
    )
    class Meta:
        model = models.CheckListItem
        fields = [
            'url',
            'uuid',
            'check_list',
            'text',
            'done',
        ]


class InnerCheckListItemSerializer(MetadataExtensionSerializer, serializers.HyperlinkedModelSerializer):
    detail_view = 'api:checkitems-detail'
    url = serializers.HyperlinkedIdentityField(
        view_name="api:checkitems-detail",
        lookup_field="uuid",
    )

    class Meta:
        model = models.CheckListItem
        fields = ['url', 'uuid', 'text', 'done']


class CheckListSerializer(MetadataExtensionSerializer, serializers.HyperlinkedModelSerializer):
    detail_view = 'api:checklists-detail'

    url = serializers.HyperlinkedIdentityField(
        view_name=detail_view,
        lookup_field="uuid",
    )
    task = serializers.HyperlinkedRelatedField(
        queryset=models.Task.objects.all(),
        view_name="api:tasks-detail",
        lookup_field="uuid",
    )
    check_items = InnerCheckListItemSerializer(many=True)

    class Meta:
        model = models.CheckList
        fields = [
            'url',
            'uuid',
            'name',
            'task',
            'check_items',
        ]


class TaskSerializer(MetadataExtensionSerializer, serializers.ModelSerializer):
    '''
    Task model serializer

    *check_list - `CheckList` many <--> one `Task` relationship
    '''
    lookup_field: str = 'uuid'
    detail_view: str = 'api:tasks-detail'

    url = serializers.HyperlinkedIdentityField(
        view_name=detail_view,
        lookup_field="uuid",
    )
    check_lists = serializers.HyperlinkedRelatedField(
        queryset=models.CheckList.objects.all(),
        many=True,
        lookup_field = 'uuid',
        view_name='api:checklists-detail'
    )
    author = serializers.HyperlinkedRelatedField(
        queryset=Users.models.Profile.objects.all(),
        lookup_field = 'uuid',
        view_name='api:profiles-detail',
    )
    executors = serializers.HyperlinkedRelatedField(
        queryset=Users.models.Profile.objects.all(),
        lookup_field = 'uuid',
        view_name='api:profiles-detail',
        many=True,
    )


    def update(self, instance: models.Task, validated_data: dict):
        '''
        update validation
        * prevents=s setting to task its own pk
        '''
        if 'parent_task' in validated_data and instance == validated_data['parent_task']:
            raise exceptions.APIException(
                code=status.HTTP_400_BAD_REQUEST,
                detail='Not allowed to put task own uuid into `parent_task` field'
            )
        return super().update(instance, validated_data)

    class Meta:
        model = models.Task
        fields = [
            'url',
            'uuid',
            'created',
            'updated',
            'deadline',
            'title',
            'description',
            'author',
            'executors',
            'done',
            'done_dt',
            'sub_tasks',
            'parent_task',
            'check_lists',
        ]
