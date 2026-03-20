from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RoleViewSet, PermissionViewSet, CreateUserAPIView, UserUpdateProfileViewSet, LoginView, LogoutView

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'profile', UserUpdateProfileViewSet)

urlpatterns = [
    path('register/', CreateUserAPIView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls))
]
