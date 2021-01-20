from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


# Create your models here.

class User(AbstractUser):
    # to log with email
    # email overwrite to be unique
    # removed from required fields list
    username_validator = UnicodeUsernameValidator()
    # override username to be blank and nullable
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        blank=True,
        null=True,
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    email = models.EmailField('email address', unique=True)
    # just for super user
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    def __str__(self):
        # shows the owner of the event (as the part of the email before the "@").
        return self.email.split('@')[0]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
