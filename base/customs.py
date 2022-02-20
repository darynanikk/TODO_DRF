from django.db.models import Manager


class ReportTaskManager(Manager):
    def custom_filter(self, *args, **kwargs):
        updated_kwargs = {k: v for k, v in kwargs.items() if v is not None}
        return super().filter(*args, **updated_kwargs)