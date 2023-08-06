# Imports from Django.  # NOQA
from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url


# Imports from other dependencies.
from rest_framework.documentation import include_docs_urls

# Imports from inspections.
from editorial_staff.api.versions.v1.urls import urlpatterns as api_v1
from editorial_staff.api.versions.v2.router import urlpatterns as api_v2


API_NAME = getattr(settings, 'STAFF_API_NAME', 'Staff API')

# We use double braces in the initial formula so we can call .format() twice.
API_TITLE = '{} (version {{}})'.format(API_NAME)


urlpatterns = [
    # API views.
    url(r'', include(api_v1, namespace='api_fallback')),

    url(r'^v1/', include(api_v1, namespace='v1')),
    # No docs for non REST-based v1.

    url(r'^v2/', include(api_v2, namespace='v2')),
    url(r'^v2/docs/',
        include_docs_urls(
            title=API_TITLE.format('2'),
            patterns=api_v2,
            schema_url='/api/v2/'
        )),
]
