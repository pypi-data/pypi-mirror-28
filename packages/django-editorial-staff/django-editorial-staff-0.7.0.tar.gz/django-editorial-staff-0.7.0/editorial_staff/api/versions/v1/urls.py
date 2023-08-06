# Imports from Django.  # NOQA
from django.conf.urls import include
from django.conf.urls import url


# Imports from editorial-staff.  # NOQA
from editorial_staff.api.versions.v1 import views as api_views


urlpatterns = [
    url(r'^$', api_views.RootAPIView.as_view(), name='root'),
    url(r'^staff/', include([
        url(
            r'^$',
            api_views.StaffList.as_view(),
            name='staffer-list'
        ),
        url(
            r'^rescrape/(?P<email>.+)/$',
            api_views.StaffRescrape.as_view(),
            name='staffer-rescrape'
        ),
        url(
            r'^(?P<email>.+)/$',
            api_views.StaffFetch.as_view(),
            name='staffer-detail'
        ),
    ])),
    url(r'^hub/', include([
        url(
            r'^$',
            api_views.HubList.as_view()
        ),
        url(
            r'^(?P<slug>.+)/$',
            api_views.HubFetch.as_view()
        ),
    ])),
    url(r'^vertical/', include([
        url(
            r'^$',
            api_views.VerticalList.as_view()
        ),
        url(
            r'^(?P<slug>.+)/$',
            api_views.VerticalFetch.as_view()
        ),
    ])),
]
