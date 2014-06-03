import os
__version__ = '0.1.0'
# Get Some Defaults
AKAMAI_USERNAME     =   os.environ.get('AKAMAI_USERNAME', None)
AKAMAI_PASSWORD     =   os.environ.get('AKAMAI_PASSWORD', None)
AKAMAI_NOTIFY_EMAIL =   os.environ.get('AKAMAI_NOTIFY_EMAIL', None)

django_settings =   False
try:
    from django.conf import settings as django_settings
except:
    pass

if django_settings:
    try:
        AKAMAI_USERNAME     =   getattr(django_settings, 'AKAMAI_USERNAME', AKAMAI_USERNAME)
        AKAMAI_PASSWORD     =   getattr(django_settings, 'AKAMAI_PASSWORD', AKAMAI_PASSWORD)
        AKAMAI_NOTIFY_EMAIL =   getattr(django_settings, 'AKAMAI_NOTIFY_EMAIL', AKAMAI_NOTIFY_EMAIL)
    except:
        pass # this isn't being run inside a Django environment

from api import APIRequest
__all__ =   ['api', 'cli_ccu', 'APIRequest']

