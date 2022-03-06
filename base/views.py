from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from base.filters import CustomTaskFilter
from base.models import Task, Attachment, Category
from base.reports import task_report
from base.serializers import (WriteTaskSerializer, ReadTaskSerializer, CategorySerializer, AttachmentSerializer,
                              ReportTaskSerializer, ParamsTaskSerializer)


class AttachmentList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AttachmentSerializer
    queryset = Attachment.objects.all()


class TaskModelView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomTaskFilter

    def get_queryset(self):
        return Task.objects.select_related("category", "owner").filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method in "GET":
            return ReadTaskSerializer
        return WriteTaskSerializer


class CategoryList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()


class TaskReportView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    data = {}

    def get(self, request, *args, **kwargs):
        serializer_params = ParamsTaskSerializer(data=request.GET, context={"request": request})
        serializer_params.is_valid(raise_exception=True)
        params = serializer_params.save()
        data = task_report(params)
        serializer = ReportTaskSerializer(instance=data, many=True)
        return Response(data=serializer.data)


class TasksByTagName(generics.ListAPIView):
    serializer_class = ReadTaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(tags__name=self.kwargs['tag_name'])