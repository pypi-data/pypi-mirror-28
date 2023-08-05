from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from django.utils.translation import ugettext_lazy as _


class TimeStampMixin(object):
    class Meta:
        get_latest_by = 'modified'
        ordering = ('-modified', '-created',)

    created = CreationDateTimeField(_('created'))
    modified = ModificationDateTimeField(_('modified'))