from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from base.filters import CustomTaskFilter
from base.reports import task_report
from base.serializers import (WriteTaskSerializer, ReadTaskSerializer, CategorySerializer, TagSerializer, AttachmentSerializer, ReportTaskSerializer, ParamsTaskSerializer)
from rest_framework import generics, viewsets
from base.models import Task, Category, Tag, Attachment


class TagList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class AttachmentList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AttachmentSerializer
    queryset = Attachment.objects.all()


class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomTaskFilter
    # This was missing

    def get_queryset(self):
        return Task.objects.select_related("category", "owner").filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadTaskSerializer
        return WriteTaskSerializer


class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()

class TaskReportAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    data = {}

    def get(self, request):
        serializer_params = ParamsTaskSerializer(data=request.GET, context={"request": request})
        serializer_params.is_valid(raise_exception=True)
        params = serializer_params.save()
        data = task_report(params)
        serializer = ReportTaskSerializer(instance=data, many=True)
        return Response(data=serializer.data)

