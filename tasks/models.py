from django.db import models

# Create your models here.

from mongoengine import Document, StringField, BooleanField

class Task(Document):
    title = StringField(required=True, max_length=200)
    description = StringField()
    completed = BooleanField(default=False)
