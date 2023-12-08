from django.urls import path
from django.conf.urls import include
from .views import (
    account_inactive,
    id_duplicate_check,
)


urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('account-inactive/', account_inactive, name='account_inactive'),
    path('id-duplicate-check/', id_duplicate_check, name='id_duplicate_check'),
]