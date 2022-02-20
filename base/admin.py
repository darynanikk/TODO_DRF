from django.contrib import admin
from base.models import Task, Category, Subtask, Tag, Attachment


# Register your models here.
admin.site.register(Task)
admin.site.register(Category)
admin.site.register(Subtask)
admin.site.register(Tag)
admin.site.register(Attachment)