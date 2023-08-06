# Imports from other dependencies.  # NOQA
from rest_framework import viewsets


# Imports from editorial-staff.
from editorial_staff.api.versions.v2.mixins import CaseInsensitiveLookupMixin
from editorial_staff.api.versions.v2.serializers import HubSerializer
from editorial_staff.api.versions.v2.serializers import StafferSerializer
from editorial_staff.api.versions.v2.serializers import VerticalSerializer
from editorial_staff.models import Hub
from editorial_staff.models import Staffer
from editorial_staff.models import Vertical


class VerticalViewSet(CaseInsensitiveLookupMixin,
                      viewsets.ReadOnlyModelViewSet):
    """"""
    lookup_field = 'slug'
    queryset = Vertical.objects.all()
    serializer_class = VerticalSerializer


class HubViewSet(CaseInsensitiveLookupMixin, viewsets.ReadOnlyModelViewSet):
    """"""
    lookup_field = 'slug'
    queryset = Hub.objects.all()
    serializer_class = HubSerializer


class StafferViewSet(CaseInsensitiveLookupMixin,
                     viewsets.ReadOnlyModelViewSet):
    """"""
    lookup_field = 'email'
    queryset = Staffer.objects.all()
    serializer_class = StafferSerializer

    # The following line is needed because Django Rest Framework doesn't allow
    # periods or @-signs in the default regex it uses to parse detail URLs.
    lookup_value_regex = '[0-9A-Za-z@.]+'

    # TODO(ajv): Extend get_object to recreate previous fetch behavior:
    # "If user not found, query slack and create user if email exists."
    # Should return a 201 if that's the case.

    # TODO(ajv): Add a 'rescrape' route that passes back raw and formatted
    # staffer data (based on what is listed in Slack) given a user's email.
