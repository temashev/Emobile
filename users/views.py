from django.contrib.auth import logout, authenticate, login
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import User, Role, Permission
from .permissions import GlobalPermission, IsOwnerOrReadOnly
from .serializers import UserRegisterSerializer, RoleSerializer, PermissionSerializer, UserSerializer, \
    UserUpdateProfileSerializer


class CreateUserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    resource_name = 'role'
    permission_classes = [GlobalPermission]


class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(is_active=True).all()    # для показа только юзеров с флагом is_active
    serializer_class = UserSerializer
    resource_name = 'user'
    permission_classes = [GlobalPermission]


class UserUpdateProfileViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserUpdateProfileSerializer
    resource_name = 'profile'
    permission_classes = [IsOwnerOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        """ Переопределение метода для деактивации аккаунта с 'мягким удалением' """
        instance = self.get_object()

        # Возможность удаления из БД для админа
        if request.user.role.name == 'Админ':
            instance.delete()
            return Response({'detail': 'Пользователь удален из БД'}, status=HTTP_204_NO_CONTENT)

        # логика для обычного пользователя
        instance.is_active = False  # Смена флага для мягкого удаления
        instance.save()  # Сохранение пользователя

        logout(request)  # Выход пользователя из системы

        return Response({'detail': 'Аккаунт удален, сеанс завершен'}, status=HTTP_204_NO_CONTENT)


class LoginView(APIView):
    """ Вход пользователя в систему """
    permission_classes = []  # пустой, т.к. вход разрешен абсолютно всем

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return Response({'detail': f'Вход выполнен успешно. Данные: {user.fio}'}, status=HTTP_200_OK)

        return Response({'detail': 'Данные введены неверно'}, status=HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """ Выход пользователя из системы """
    def post(self, request):
        logout(request)
        return Response({'detail': 'Выход из системы'}, status=HTTP_200_OK)


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [GlobalPermission]


class ProductMockView(APIView):
    permission_classes = [GlobalPermission]
    resource_name = 'products'

    def get(self, request):
        """ Список объектов-заглушек """
        data = [
            {'id': 1, 'name': 'Смартфон Nothing Phone (1)', 'price': 30000},
            {'id': 2, 'name': 'Видеокарта Palit RTX 3070', 'price': 40000},
        ]
        return Response(data)

    def post(self, request):
        """ Создание объекта """
        return Response({'detail': 'Товар создан'}, status=HTTP_201_CREATED)
