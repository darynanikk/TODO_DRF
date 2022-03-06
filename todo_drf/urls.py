from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('login/', obtain_auth_token),
    path('admin/', admin.site.urls),
    path('', include('base.urls'))
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]