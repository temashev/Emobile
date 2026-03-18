from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

ACTION_CHOICES = [
    ('view', 'Просмотр'),
    ('create', 'Создание'),
    ('delete', 'Удаление'),
    ('update', 'Обновление')
]


class UserManager(BaseUserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Нужно обязательно указать Email')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Хэширование пароля
        user.save(using=self._db)
        return user


class Permission(models.Model):
    name = models.CharField(max_length=20, verbose_name='Право')
    action = models.CharField(choices=ACTION_CHOICES, verbose_name='Действие')
    resource = models.CharField(max_length=50, verbose_name='Ресурс')

    class Meta:
        verbose_name = 'Право'
        verbose_name_plural = 'Права'

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='Роль')
    description = models.TextField(max_length=250, blank=True, verbose_name='Описание')
    permissions = models.ManyToManyField(Permission, verbose_name='Права')

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    fio = models.CharField(max_length=100, verbose_name='ФИО')
    is_active = models.BooleanField(default=True)

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Роль')

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fio']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
