from mongoengine import *
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

# from .query import ReportQuerySet


class Event(Document):
    project = StringField(max_length=200)
    device = StringField(max_length=200)
    site = StringField(max_length=200)
    camera = StringField(max_length=200)
    time = DateTimeField(required=True)
    path = StringField(max_length=200, required=True)
    event = StringField(max_length=200, required=True)
    slot = StringField(max_length=200)

    meta = {"db_alias": "metz-db-alias", "collection": "event"}

    def __str__(self):
        return self.project

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
