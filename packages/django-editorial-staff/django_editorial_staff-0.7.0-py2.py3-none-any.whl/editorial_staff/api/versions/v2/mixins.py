# Imports from Django.  # NOQA
from django.shortcuts import get_object_or_404


class CaseInsensitiveLookupMixin(object):
    """A mixin to allow for case-insensitive URL param filtering.

    The poster of of this mixin on StackOverflow says he "stole" the
    "majority" of its logic from the following location:

    http://www.django-rest-framework.org/api-guide/generic-views/
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {self.lookup_field: self.kwargs[self.lookup_field].lower()}

        return get_object_or_404(queryset, **filter)  # Lookup the object
