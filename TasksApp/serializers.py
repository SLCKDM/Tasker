from rest_framework import serializers
from rest_framework import exceptions
from rest_framework import status
from rest_framework.fields import empty
from rest_framework.exceptions import ErrorDetail, ValidationError

from . import models
import Users.models
import Tasker.serializers
import Users.serializers


class CurrentUserDefault():
    requires_context = True

    def __call__(self, field):
        return field.context['request'].user


class CheckListItemSerializer(
    serializers.HyperlinkedModelSerializer
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:checkitems-detail",
        lookup_field="uuid",
    )
    check_list = serializers.HyperlinkedRelatedField(
        view_name='api:checklists-detail',
        queryset=models.CheckList.objects.all(),
        lookup_field="uuid"
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


class InnerCheckListItemSerializer(
    serializers.HyperlinkedModelSerializer
):
    detail_view = 'api:checkitems-detail'

    url = serializers.HyperlinkedIdentityField(
        view_name="api:checkitems-detail",
        lookup_field="uuid",
    )

    class Meta:
        model = models.CheckListItem
        fields = [
            'url',
            'uuid',
            'text',
            'done'
        ]


class CheckListSerializer(
    serializers.HyperlinkedModelSerializer
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:checklists-detail",
        lookup_field="uuid",
    )
    task = serializers.HyperlinkedRelatedField(
        view_name='api:tasks-detail',
        queryset=models.Task.objects.all(),
        lookup_field="uuid"
    )
    check_items = serializers.HyperlinkedRelatedField(
        view_name='api:checkitems-detail',
        queryset=models.CheckListItem.objects.all(),
        lookup_field="uuid",
        many=True
    )

    class Meta:
        model = models.CheckList
        fields = [
            'url',
            'uuid',
            'name',
            'task',
            'check_items',
        ]


class SubTaskSerializer(
    serializers.ModelSerializer,
):
    '''
    Task model serializer

    *check_list - `CheckList` many <--> one `Task` relationship
    '''

    url = serializers.HyperlinkedIdentityField(view_name="api:tasks-detail", lookup_field="uuid")

    class Meta:
        model = models.Task
        fields = [
            'url'
        ]


class TaskSerializer(
    serializers.ModelSerializer,
):
    '''
    Task model serializer
    '''
    url = serializers.HyperlinkedIdentityField(
        view_name="api:tasks-detail",
        lookup_field="uuid"
    )
    check_lists = serializers.HyperlinkedRelatedField(
        view_name='api:checklists-detail',
        queryset=models.CheckList.objects.all(),
        lookup_field="uuid",
        many=True
    )
    child_tasks = serializers.HyperlinkedRelatedField(
        view_name='api:tasks-detail',
        queryset=models.Task.objects.all(),
        lookup_field="uuid",
        many=True
    )
    parent_task = serializers.HyperlinkedRelatedField(
        view_name='api:tasks-detail',
        queryset=models.Task.objects.all(),
        lookup_field="uuid",
        allow_null=True,
        required=False
    )
    author = serializers.HyperlinkedRelatedField(
        view_name='api:profiles-detail',
        queryset=Users.models.Profile.objects.all(),
        lookup_field="uuid",
        required=False
    )
    executors = serializers.HyperlinkedRelatedField(
        view_name='api:profiles-detail',
        queryset=Users.models.Profile.objects.all(),
        lookup_field="uuid",
        many=True
    )

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
            'child_tasks',
            'parent_task',
            'check_lists',
        ]

    def update(self, instance, validated_data):
        if instance in validated_data.get('child_tasks', []):
            raise ValidationError('Task can`t be subtask for itself', status.HTTP_406_NOT_ACCEPTABLE)
        return super().update(instance, validated_data)
