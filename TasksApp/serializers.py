from rest_framework import serializers

from . import models
import Users.models

class CheckListItemSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    text = serializers.CharField(max_length=300, required=True)
    done = serializers.BooleanField()
    check_list = serializers.PrimaryKeyRelatedField(
        queryset=models.CheckList.objects.all(),
        required=True
    )

    class Meta:
        model = models.CheckListItem
        fields = [
            'uuid',
            'text',
            'done',
            'check_list',
        ]

class InnerCheckListItemSerializer(serializers.HyperlinkedModelSerializer):
    uuid = serializers.UUIDField()
    text = serializers.CharField(max_length=300)
    done = serializers.BooleanField()

    class Meta:
        model = models.CheckListItem
        fields = ['uuid', 'text', 'done']


class CheckListSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=200, required=True)
    check_items = InnerCheckListItemSerializer(many=True)
    task = serializers.PrimaryKeyRelatedField(
        queryset=models.Task.objects.all(),
        required=True
    )

    class Meta:
        model = models.CheckList
        fields = [
            'uuid',
            'name',
            'check_items',
            'task',
        ]


class TaskSerializer(serializers.ModelSerializer):

    uuid = serializers.UUIDField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    deadline = serializers.DateTimeField(allow_null=True)
    title = serializers.CharField(max_length=200, required=True)
    description = serializers.CharField(max_length=1000)

    done = serializers.BooleanField()
    done_dt = serializers.DateTimeField(allow_null=True)
    parent_task = serializers.PrimaryKeyRelatedField(
        queryset=models.Task.objects.all(),
        allow_null=True,
    )
    sub_tasks = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Task.objects.all(),
        allow_null=True
    )
    check_lists = serializers.PrimaryKeyRelatedField(
        queryset=models.CheckList.objects.all(),
        many=True,
        allow_null=True,
    )
    author = serializers.PrimaryKeyRelatedField(
        queryset=Users.models.Profile.objects.all()
    )
    executors = serializers.PrimaryKeyRelatedField(
        queryset=Users.models.Profile.objects.all(),
        many=True,
    )

    def update(self, instance, validated_data):
        if instance == validated_data['parent_task']:
            raise NotImplementedError('Not allowed to put tasks own uuid into `parent_task` field')
        return super().update(instance, validated_data)

    class Meta:
        model = models.Task
        fields = [
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
            'check_lists'
        ]