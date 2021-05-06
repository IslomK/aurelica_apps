from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/aurelica/', include('api.urls')),
    path('query_api/v1/aurelica/', include('query_api.urls')),
]
