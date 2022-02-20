from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from base.views import (
    CategoryModelViewSet,
    TaskModelViewSet,
    TagList,
    AttachmentList,
    TaskReportAPIView,
)
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'tasks', TaskModelViewSet, basename="task")
router.register(r'categories', CategoryModelViewSet, basename="category")

urlpatterns = [
    path('login/', obtain_auth_token),
    path('admin/', admin.site.urls),
    path('tags/', TagList.as_view()),
    path('attachments/', AttachmentList.as_view()),
] + router.urls

urlpatterns += [
    path('report/', TaskReportAPIView.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]