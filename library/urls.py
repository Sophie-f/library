from django.urls import include,path
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('reserve.urls')),
    path('payment',include('reserve.urls'))
]
