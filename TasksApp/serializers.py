from rest_framework import serializers
from rest_framework import exceptions
from rest_framework import status

from . import models
import Users.models
import Tasker.serializers


class CurrentUserDefault():
    requires_context = True

    def __call__(self, field):
        return field.context['request'].user


class CheckListItemSerializer(
    serializers.HyperlinkedModelSerializer
):
    detail_view = 'api:checkitems-detail'

    meta = Tasker.serializers.MetadataField(view_name=detail_view)
    check_list = Tasker.serializers.MetadataRelatedField(
        queryset = models.CheckList.objects.all(),
        view_name = "api:checklists-detail",
        lookup_field = "uuid"
    )
    class Meta:
        model = models.CheckListItem
        fields = [
            'meta',
            'uuid',
            'check_list',
            'text',
            'done',
        ]


class InnerCheckListItemSerializer(
    serializers.HyperlinkedModelSerializer
):
    detail_view = 'api:checkitems-detail'

    meta = Tasker.serializers.MetadataField(view_name=detail_view)
    url = serializers.HyperlinkedIdentityField(
        view_name="api:checkitems-detail",
        lookup_field="uuid",
    )

    class Meta:
        model = models.CheckListItem
        fields = [
            'meta',
            'url',
            'uuid',
            'text',
            'done'
        ]
        metadata_fields = ['url', 'object_type', 'object_type']


class CheckListSerializer(
    serializers.HyperlinkedModelSerializer
):
    detail_view = 'api:checklists-detail'

    meta = Tasker.serializers.MetadataField(view_name=detail_view)
    task = Tasker.serializers.MetadataRelatedField(
        view_name='api:tasks-detail',
        many=False,
        lookup_field='uuid',
        queryset=models.Task.objects.all()
    )
    check_items = Tasker.serializers.MetadataRelatedField(
        view_name='api:checkitems-detail',
        many=True,
        lookup_field='uuid',
        queryset=models.Task.objects.all()
    )

    class Meta:
        model = models.CheckList
        fields = [
            'meta',
            'uuid',
            'name',
            'task',
            'check_items',
        ]


class TaskSerializer(
    # Tasker.serializers.MetadataExtensionSerializer,
    serializers.ModelSerializer
):
    '''
    Task model serializer

    *check_list - `CheckList` many <--> one `Task` relationship
    '''
    lookup_field: str = 'uuid'
    detail_view: str = 'api:tasks-detail'
    users_qset = Users.models.Profile.objects.select_related().all()
    meta = Tasker.serializers.MetadataField(view_name=detail_view)

    # check_lists = serializers.HyperlinkedRelatedField(
    #     queryset=models.CheckList.objects.filter(task=None).all(),
    #     many=True,
    #     lookup_field = 'uuid',
    #     view_name='api:checklists-detail'
    # )
    # author = serializers.HyperlinkedRelatedField(
    #     queryset=users_qset,
    #     lookup_field = 'uuid',
    #     view_name='api:profiles-detail',
    #     default=CurrentUserDefault
    # )
    # executors = serializers.HyperlinkedRelatedField(
    #     queryset=users_qset,
    #     lookup_field = 'uuid',
    #     view_name='api:profiles-detail',
    #     many=True,
    # )

    sub_tasks = Tasker.serializers.MetadataRelatedField(
        view_name='api:tasks-detail',
        many=True,
        lookup_field=lookup_field,
        read_only=True
    )
    parent_task = Tasker.serializers.MetadataRelatedField(
        view_name='api:tasks-detail',
        many=False,
        lookup_field=lookup_field,
        queryset=models.Task.objects.all()
    )
    check_lists = Tasker.serializers.MetadataRelatedField(
        queryset=models.CheckList.objects.filter(task=None).all(),
        many=True,
        lookup_field = 'uuid',
        view_name='api:checklists-detail'
    )
    author = Tasker.serializers.MetadataRelatedField(
        queryset=users_qset,
        lookup_field = 'uuid',
        view_name='api:profiles-detail',
        default=CurrentUserDefault
    )
    executors = Tasker.serializers.MetadataRelatedField(
        queryset=users_qset,
        lookup_field = 'uuid',
        view_name='api:profiles-detail',
        many=True,
    )

    def to_representation(self, instance):
        return super().to_representation(instance)

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
            'meta',
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
