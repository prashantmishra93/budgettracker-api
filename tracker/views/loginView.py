from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import UserSerializer
from budget_tracker.utility import Utility

class LoginView(APIView):
    authentication_classes = []  # diabled all authentication and disables JWT validation
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Utility.returnFormat(
                message_type='success_msg',
                data={'data' : UserSerializer(user).data, 'refresh' : str(refresh), 'access' : str(refresh.access_token)},
                query='login_query',
                http_status_code=status.HTTP_200_OK
            )
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)