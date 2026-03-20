from rest_framework import permissions


class GlobalPermission(permissions.BasePermission):
    """
    Класс для проверки глобальных прав ролей пользователей
    - проверяет вход пользователя
    - дает полный доступ для админа
    - извлекает имя ресурса из View для мапппинга
    - сопоставляет записи прав для нужной роли пользователя
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            # Если пользователь не залогинен - он не получит доступ
            return False

        # если пользователь Админ - есть доступ ко всему
        if request.user.role.name == 'Админ':
            return True

        # Словарь с методами для быстрого соотношения Метод - ресурс
        methods = {
            'GET': 'view',
            'POST': 'create',
            'PUT': 'update',
            'PATCH': 'update',
            'DELETE': 'delete',
        }

        action = methods.get(request.method)  # Извлечение метода для действия
        resource = getattr(view, 'resource_name', None)  # Извлечение ресурса при его наличии

        if not request.user.role:
            # Если у юзера нет роли - не давать доступ
            return False
        # Фильтр юзеров по Действию -Методу для выдачи прав
        return request.user.role.permissions.filter(action=action, resource=resource).exists()


class IsOwnerOrReadOnly(permissions.BasePermission):
    """ Класс проверки доступа для конкретных объектов """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Полный доступ для админа
        if request.user.role.name == 'Админ':
            return True

        return obj == request.user
