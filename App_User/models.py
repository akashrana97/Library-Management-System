from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('LIBRARIAN', 'Librarian'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')

    groups = models.ManyToManyField('auth.Group', verbose_name='groups', blank=True, related_name='app_library_users',
                                    related_query_name='app_library_user', )
    user_permissions = models.ManyToManyField('auth.Permission', verbose_name='user permissions', blank=True,
                                              help_text='Specific permissions for this user.',
                                              related_name='app_library_user_permissions',
                                              related_query_name='app_library_user_permission', )
