from django_extensions.db.models import TimeStampedModel


class TimeStampModel(TimeStampedModel):
    class Meta:
        abstract = True
