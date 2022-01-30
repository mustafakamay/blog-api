import uuid
import os
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin, Group
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):  # ability to create user and superuser

    def create_user(self, email, password=None, **extra_fields):
        # extra_fields = yeni fields eklendiğinde onları da alıp flexible olur
        """"Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email addresses')
        # normalized_email lowers domain part of email!!
        user = self.model(email=self.normalize_email(
            email),  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email,  password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """"Custom user model supports email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    objects = UserManager()  # creates new UserManager for our object

    USERNAME_FIELD = 'email'  # assign email as username for login
    phone_number = models.BigIntegerField(_('phone number'), blank=True, unique=True, null=True,
                                          validators=[MinValueValidator(1000000), MaxValueValidator(10000000000 - 1)])

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.first_name + " " + self.last_name
