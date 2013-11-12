from django.db import models
from django.contrib.auth import models as auth_models

from datetime import datetime, timedelta

class Message(models.Model):
    author = models.ForeignKey(auth_models.User)
    date = models.DateTimeField(null=True)
    title = models.CharField(max_length=50)
    text = models.TextField()

