from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField


class TimeStampMixin(object):
    class Meta:
        get_latest_by = 'modified'
        ordering = ('-modified', '-created',)
        abstract = True

    created = CreationDateTimeField(_('created'))
    modified = ModificationDateTimeField(_('modified'))