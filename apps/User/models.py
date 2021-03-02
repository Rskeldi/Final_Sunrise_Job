import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.User.send_mail import send_confirmation_email


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class AbstractEmailUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email адрес'), max_length=255, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('Дата добавления'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        abstract = True
        ordering = ['email']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def email_user(self):
        return send_confirmation_email(self)


class User(AbstractEmailUser):

    first_name = models.CharField(_('Имя'), max_length=255)
    last_name = models.CharField(_('Фамилия'), max_length=255)
    activation_code = models.CharField(max_length=36, blank=True)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.email} - {self.first_name} {self.last_name}'

    def create_activation_code(self):
        self.activation_code = str(uuid.uuid4())
