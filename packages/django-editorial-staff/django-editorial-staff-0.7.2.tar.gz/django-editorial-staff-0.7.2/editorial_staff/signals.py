# Imports from Django.  # NOQA
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.module_loading import import_string


# Imports from editorial-staff.
from editorial_staff.models import Staffer


PROVIDER_MODULE = getattr(settings, 'STAFF_DATA_PROVIDER', None)
PROVIDER_OPTIONS = {}

DATA_PROVIDER = None
if PROVIDER_MODULE is not None:
    try:
        DataProviderClass = import_string(PROVIDER_MODULE)
        DATA_PROVIDER = DataProviderClass()
        PROVIDER_OPTIONS = getattr(settings, 'STAFF_DATA_PROVIDER_OPTIONS', {})
    except ImportError:
        pass


@receiver(post_save, sender=Staffer)
def notify_slack_on_staffer_create(sender, instance, created, **kwargs):
    """"""
    if created:
        if DATA_PROVIDER is not None:
            DATA_PROVIDER.post_new_staffer_message(PROVIDER_OPTIONS, instance)
