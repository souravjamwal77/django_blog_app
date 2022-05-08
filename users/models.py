# -*- coding: utf-8 -*-
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class CustomAccountManager(BaseUserManager):
    """Custom manager for custom user model."""

    def create_user(self, email, mobile, password, **other_fields):
        """Override the create_user django method.

        Args:
            email (str): email of the user
            mobile (int): phone number of the user
            first_name (str): First name of the user
            password (str): password of the user

        Raises:
            ValueError: Raises error if email is not provided or if email is not in the correct format

        Returns:
            user: user model to the super class
        """
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=email, mobile=mobile, **other_fields)
        password = make_password(password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile, password, **other_fields):
        """Override the create_superuser django method."""
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, mobile, password, **other_fields)


class NewUser(AbstractBaseUser, PermissionsMixin):
    """Custom User model to override the django User models."""

    email = models.EmailField(_("Email address"), unique=True)
    user_name = models.CharField(_("User name"), max_length=50, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    mobile = PhoneNumberField(unique=True, null=False, blank=False)

    is_user = models.BooleanField(default=False)
    is_merchant = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_("about"), max_length=500, blank=True)

    # Django admin fields
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["mobile"]

    def __str__(self):
        return self.user_name
