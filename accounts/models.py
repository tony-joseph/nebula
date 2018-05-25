import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """Create and save a user with the given username, email, and password."""

    def _create_user(self, email, first_name, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, first_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, first_name, password, **extra_fields)

    def create_superuser(self, email, first_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, first_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'
    GENDER_OTHER = 'other'
    GENDER_NOT_SPECIFIED = 'not specified'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
        (GENDER_NOT_SPECIFIED, 'Not specified'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, blank=True, default='')
    email = models.EmailField(unique=True, db_index=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    about_me = models.TextField(blank=True, default='', max_length=10000)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=32, choices=GENDER_CHOICES, default=GENDER_NOT_SPECIFIED)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='accounts/users/profile-pictures')

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', ]

    objects = UserManager()

    def __str__(self):
        return str(self.email)

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return str(self.first_name)
