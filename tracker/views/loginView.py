from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import UserSerializer
from budget_tracker.utility import Utility
import logging
logger = logging.getLogger(__name__)

class LoginView(APIView):
    authentication_classes = []  # diabled all authentication and disables JWT validation
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = authenticate(request,username=username, password=password)
            logger.info("DATA NOT GET =======>")
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Utility.returnFormat(
                    message_type='success_msg',
                    data={
                        'data': UserSerializer(user).data,
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    },
                    query='login_query',
                    http_status_code=status.HTTP_200_OK
                )
            else:
                return Utility.returnFormat(
                    message_type='error_msg',
                    data=[],
                    query='invalid_user',
                    http_status_code=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error("Division error occurred", exc_info=True)
            return Utility.returnFormat(
                message_type='error_msg',
                data=[],
                query='validation_error',
                http_status_code=status.HTTP_400_BAD_REQUEST
            )