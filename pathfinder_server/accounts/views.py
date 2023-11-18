
from django.http import JsonResponse
from rest_framework import status

from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.generics import (
    CreateAPIView,
)


def account_inactive(request):
    return JsonResponse(
        {'message':'Your account is inactive. \
                    Please wait for admin approval.'},
        status=status.HTTP_401_UNAUTHORIZED
    )