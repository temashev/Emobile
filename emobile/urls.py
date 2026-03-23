from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# swagger для отладки API
# с учетом фидбека, я разобрался с данной технологией
# теперь в проекте есть документация для эндпоинтов
schema_view = get_schema_view(
    openapi.Info(
        title='Snippets API',
        default_version='v1',
        description='Test',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='www.tema15@gmail.com'),
        license=openapi.License(name='BSD License')
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('accounts/', include('rest_framework.urls')), # для выхода из сваггера
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
