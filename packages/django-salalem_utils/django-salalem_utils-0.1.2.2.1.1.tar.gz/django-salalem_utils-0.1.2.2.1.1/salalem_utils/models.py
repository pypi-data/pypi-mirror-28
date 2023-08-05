from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from django.utils.translation import ugettext_lazy as _


class TimeStampMixin(models.Model):
    class Meta:
        get_latest_by = 'modified'
        ordering = ('-modified', '-created',)
        abstract = True

    created = CreationDateTimeField(_('created'))
    modified = ModificationDateTimeField(_('modified'))