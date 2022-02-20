from django.db import models
from django.contrib.auth.models import User

from base.customs import ReportTaskManager


class Category(models.Model):
    owner = models.ForeignKey(User, related_name='categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=32, blank=True)
    objects = ReportTaskManager()

    def __str__(self):
        return self.name


class Tag(models.Model):
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label


class Task(models.Model):

    class Priority(models.IntegerChoices):
        URGENT = 1
        HIGH = 2
        MEDIUM = 3
        LOW = 4

    objects = ReportTaskManager()
    owner = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(choices=Priority.choices)
    category = models.ForeignKey(Category, null=True, blank=True, related_name='tasks', on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, related_name="tasks")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']


class Subtask(models.Model):
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created']


class Attachment(models.Model):
    task = models.ForeignKey(Task, related_name="attachments", on_delete=models.CASCADE)
    upload = models.FileField(upload_to="uploads/")

    def __str__(self):
        return f"upload to task {self.task.title}"
