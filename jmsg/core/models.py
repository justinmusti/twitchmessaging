from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from django.conf import settings


class User(AbstractUser):
    pass


class Conversation(models.Model):

    id = models.UUIDField(primary_key=True, unique=True, null=False, blank=False, default=uuid4)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False,
                               related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False,
                                 related_name='receiver')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, null=False, blank=False, default=uuid4)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
    text = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
