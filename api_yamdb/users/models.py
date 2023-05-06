from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constaints import EMAIL_LENGTH, USER_FIELDS_LENGTH


class User(AbstractUser):

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    ]
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    email = models.EmailField(unique=True, blank=False,
                              max_length=EMAIL_LENGTH)
    role = models.CharField(
        choices=ROLES,
        default=USER,
        max_length=10,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=USER_FIELDS_LENGTH,
        null=True,
        unique=True
    )
    first_name = models.CharField(max_length=USER_FIELDS_LENGTH, blank=True)
    last_name = models.CharField(max_length=USER_FIELDS_LENGTH, blank=True)

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    class Meta:

        ordering = ['username']
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username
