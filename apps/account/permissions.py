from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from apps.account.models import PrimaryToken


class PrimaryTokenPermission(BasePermission):

    def has_permission(self, request: Request, view):
        given_token = request.headers.get('X-Access-Token')

        if not given_token:
            return False

        token_obj = PrimaryToken.objects.filter(token=given_token, is_active=True).first()

        return token_obj is not None
