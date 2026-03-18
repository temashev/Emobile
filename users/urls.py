from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RoleViewSet, PermissionViewSet, CreateUserAPIView


router = DefaultRouter
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)

urlpatterns = [
    path('register/', CreateUserAPIView.as_view(), name='register'),
    path('', include(router.urls))
]
