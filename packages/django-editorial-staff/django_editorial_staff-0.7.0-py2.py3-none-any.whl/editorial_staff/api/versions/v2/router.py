# Imports from other dependencies.  # NOQA
from rest_framework import routers


# Imports from inspections.
from editorial_staff.api.versions.v2.views import HubViewSet
from editorial_staff.api.versions.v2.views import StafferViewSet
from editorial_staff.api.versions.v2.views import VerticalViewSet


app_name = 'staff_api_v2'


router = routers.DefaultRouter()
router.register('hubs', HubViewSet)
router.register('staffers', StafferViewSet)
router.register('verticals', VerticalViewSet)

urlpatterns = router.urls
