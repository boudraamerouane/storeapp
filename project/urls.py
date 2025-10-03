from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, re_path
from django.views.static import serve
import os
from django.conf import settings
from store import views

urlpatterns = [
     path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('admin/', admin.site.urls),
    path('api/', include('store.urls')),  # ✅ include store app API
    re_path(r'^.*$', views.index, name='index'),
     
]
