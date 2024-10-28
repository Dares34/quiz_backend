from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class Roles(models.Model):
    id = models.IntegerField(primary_key=True, serialize=True)
    name = models.CharField(max_length=255)
    is_admin = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, role=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), name=name, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, role=None):
        user = self.create_user(email=email, name=name, password=password, role=role)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(Roles, on_delete=models.PROTECT)

    objects = UserManager()  # Указываем кастомный менеджер

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'role']

    def __str__(self):
        return self.name

