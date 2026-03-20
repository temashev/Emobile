from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, Role, Permission


class UserRegisterSerializer(serializers.ModelSerializer):
    """ Сериализатор для регистрации пользователей """
    password = serializers.CharField(write_only=True, min_length=8)  # write_only для запрета возврата пароля в ответе
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'fio', 'password', 'confirm_password', 'role']

    def validate(self, attrs):
        """ Проверка на соответсвие паролей """
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError({'password': 'Пароли не совпадают!'})
        return attrs

    def create(self, validated_data):
        """ Метод для создания юзера """
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)


class UserUpdateProfileSerializer(serializers.ModelSerializer):
    """ Сериализатор для обновления данных пользователей """
    class Meta:
        model = User
        fields = ['id', 'fio', 'password']
        extra_kwargs = {'password': {'write_only': True}}   # чтобы хэш пароля не возвращался в ответе

    def update(self, instance, validated_data):
        """ Переопределение метода для возможности редактирования профиля """
        instance.fio = validated_data.get('fio', instance.fio)  # Смена ФИО

        # Смена пароля
        new_password = validated_data.get('password')
        if new_password:
            instance.set_password(new_password)

        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
