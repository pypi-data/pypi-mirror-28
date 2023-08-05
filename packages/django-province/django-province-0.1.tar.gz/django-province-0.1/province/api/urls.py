from django.conf.urls import include, url

from province.api.views import ProvinceListAPIView, ProvinceCreateAPIView, ProvinceDetailAPIView, CityAutocomplete


urlpatterns = [
    url(r'^$', ProvinceListAPIView.as_view(), name='list'),
    url(r'^create/$', ProvinceCreateAPIView.as_view(), name='create'),
    url(r'^city/autocomplete/$', CityAutocomplete.as_view(), name='city-autocomplete', ),
    url(r'^(?P<id>\d+)/$', ProvinceDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<province_id>\d+)/city/', include('province.api.urls-city', namespace='city-api')),
    url(r'^(?P<province_id>\d+)/shahrak/', include('province.api.urls-shahrak', namespace='shahrak-api')),
]