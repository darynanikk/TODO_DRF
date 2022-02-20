from dataclasses import dataclass
import datetime
from decimal import Decimal

from django.db.models import Count, Q
from django.contrib.auth.models import User

from base.models import Subtask, Category, Task, Tag, Attachment


@dataclass
class ReportTask:
    category: Category
    completed_subtasks_count: int


@dataclass
class ReportParams:
    user: User
    start_date: datetime.datetime = None
    end_date: datetime.datetime = None
    priority: int = None
    complete: bool = False
    category_name: str = ""


def task_report(params):
    data = []
    subtask_completed = Count("subtasks", filter=Q(subtasks__complete=True))
    # filter tasks by sent params and count completed subtasks
    queryset = Task.objects.custom_filter(complete=params.complete, priority=params.priority, created__gte=params.start_date,
                                   created__lte=params.end_date, owner=params.user).values("category").annotate(
        completed_subtasks_count=subtask_completed,
    )
    categories_index = {}
    for category in Category.objects.custom_filter(owner=params.user, name=params.category_name):
        categories_index[category.pk] = category

    for entry in queryset:
        category = categories_index.get(entry["category"])
        report_entry = ReportTask(category, entry["completed_subtasks_count"])
        data.append(report_entry)

    return data
