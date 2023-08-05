from django.db import models
from django_extensions.db.models import TimeStampedModel


class TimeStampMixin(TimeStampedModel):
    class Meta:
        abstract = True
