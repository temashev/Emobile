from rest_framework.permissions import BasePermission


class GlobalPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        methods = {
            'GET': 'view',
            'POST': 'create',
            'PUT': 'update',
            'PATCH': 'update',
            'DELETE': 'delete',
        }

        action = methods.get(request.method)
        resource = getattr(view, 'resource_name', None)

        if not request.user.role:
            return False
        return request.user.role.permissions.filter(action=action, resource=resource).exists()