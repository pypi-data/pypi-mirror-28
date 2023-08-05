from django.conf.urls import include, url

from province.api.views import CityCreateAPIView, CityDetailAPIView, CityListAPIView


urlpatterns = [
    url(r'^$', CityListAPIView.as_view(), name='list'),
    url(r'^create/$', CityCreateAPIView.as_view(), name='create'),
    url(r'^(?P<id>\d+)/$', CityDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<city_id>\d+)/town/', include('province.api.urls-town', namespace='town-api')),
]