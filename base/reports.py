from dataclasses import dataclass
import datetime
from django.db.models import Count, Q
from django.contrib.auth.models import User
from base.models import Subtask, Category, Task
from taggit.models import Tag


@dataclass
class ReportTask:
    category: Category
    tag: Tag.name
    completed_subtasks_count: int


@dataclass
class ReportParams:
    user: User
    start_date: datetime.datetime = None
    end_date: datetime.datetime = None
    priority: int = None
    complete: bool = False


def task_report(params):
    data = []
    subtask_completed = Count("subtasks", filter=Q(subtasks__complete=True))
    # filter tasks by sent params and count completed subtasks
    queryset = Task.objects.custom_filter(complete=params.complete, priority=params.priority,
                                          created__gte=params.start_date,
                                          created__lte=params.end_date, owner=params.user).values("category",
                                                                                                  "tags").annotate(
        completed_subtasks_count=subtask_completed,
    )
    categories_index = {}
    tags_index = {}
    for category in Category.objects.filter(owner=params.user):
        categories_index[category.pk] = category

    for tag in Tag.objects.all():
        tags_index[tag.pk] = tag

    print(tags_index)
    for entry in queryset:
        category = categories_index.get(entry["category"])
        tag = tags_index.get(entry["tags"])
        report_entry = ReportTask(category, tag, entry["completed_subtasks_count"])
        data.append(report_entry)

    return data
