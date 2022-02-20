from django_filters import rest_framework as filters
from base.models import Task


class M2MFilter(filters.Filter):
    def filter(self, qs, value):
        if not value:
            return qs

        values = [value.strip() for value in value.split(',')]
        qs = qs.filter(tags__label__in=values)
        return qs


class CustomTaskFilter(filters.FilterSet):
    tags = M2MFilter(
        field_name='tags',
    )

    class Meta:
        model = Task
        fields = [
            'category',
            'title',
            'complete',
            'priority',
        ]
