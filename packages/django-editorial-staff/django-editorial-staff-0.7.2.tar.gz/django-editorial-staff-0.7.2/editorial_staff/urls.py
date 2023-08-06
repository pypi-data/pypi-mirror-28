# Imports from Django.  # NOQA
from django.conf.urls import include, url  # NOQA


# Imports from editorial-staff.
from editorial_staff.api.urls import urlpatterns as api_urlpatterns
from editorial_staff.views import StafferCreate
from editorial_staff.views import StafferDetail
from editorial_staff.views import Staffers as StafferList
from editorial_staff.views import StafferUpdate


app_name = 'editorial_staff'


# Admin-site views.
urlpatterns = [
    url(
        r'^$',
        StafferList.as_view(),
        name='staffer-list'
    ),
    url(
        r'^create/$',
        StafferCreate.as_view(),
        name='staffer-create'
    ),
    # TODO(ajv): Add staffer detail view.
    url(
        r'^(?P<pk>[0-9]+)/$',
        StafferDetail.as_view(),
        name='staffer-detail'
    ),
    url(
        r'^(?P<pk>[0-9]+)/edit/$',
        StafferUpdate.as_view(),
        name='staffer-edit'
    ),

    # API views.
    url(r'^api/', include(api_urlpatterns, namespace='api')),
]
