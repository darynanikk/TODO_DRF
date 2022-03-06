from rest_framework import serializers
from base.models import Task, Subtask, Category, Attachment
from django.contrib.auth.models import User
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)
from taggit.models import Tag, TaggedItem
from base.reports import ReportParams


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("owner", "name")


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ("upload",)


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = (
            "task",
            "title",
            "complete",
            "created",
        )


class ReadOnlyUserSerializer:
    class Meta:
        model = User
        fields = ("id", "username")


class ReadTaskSerializer(TaggitSerializer, serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    subtasks = SubtaskSerializer(many=True)
    attachments = AttachmentSerializer(many=True)
    owner = ReadOnlyUserSerializer()
    tags = TagListSerializerField()

    class Meta:
        model = Task
        fields = (
            "id",
            "owner",
            "title",
            "description",
            "complete",
            "created",
            "priority",
            "category",
            "tags",
            "subtasks",
            "attachments",
            "tags",
        )


class WriteTaskSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.SlugRelatedField(slug_field="name", queryset=Category.objects.all())

    class Meta:
        model = Task
        fields = (
            "owner",
            "title",
            "description",
            "complete",
            "created",
            "priority",
            "category",
        )

    # enable to create tasks under category that authenticated user created
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        owner = self.context["request"].user
        self.fields["category"].queryset = owner.categories.all()


class ReportTaskSerializer(TaggitSerializer, serializers.Serializer):
    category = CategorySerializer()
    tag = serializers.CharField(max_length=32)
    completed_subtasks_count = serializers.DecimalField(max_digits=15, decimal_places=2)


class ParamsTaskSerializer(TaggitSerializer, serializers.Serializer):
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)
    priority = serializers.IntegerField(required=False)
    complete = serializers.BooleanField(required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        return ReportParams(**validated_data)
