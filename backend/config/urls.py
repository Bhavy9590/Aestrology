from django.contrib import admin
from django.urls import path
from kundli.views import kundli_api, places_api
urlpatterns=[path("admin/",admin.site.urls),path("api/kundli/",kundli_api),path("api/places/",places_api)]
