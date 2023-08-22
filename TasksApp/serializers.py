from rest_framework import serializers

from . import models
from Users.serializers import ProfileSerializer

class TaskSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    deadline = serializers.DateTimeField(allow_null=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000)
    author = ProfileSerializer()
    done = serializers.BooleanField()
    done_dt = serializers.DateTimeField(allow_null=True)
    # sub_tasks = serializers.PrimaryKeyRelatedField(many=True, allow_null=True)
    executors = ProfileSerializer(many=True, allow_null=True)

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
            'done',
            'done_dt',
            # 'sub_tasks',
            'executors',
        ]