from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..serializers import RegisterSerializer, UserSerializer
from budget_tracker.utility import Utility

class RegisterView(APIView):
    authentication_classes = []  # diabled all authentication and disables JWT validation
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Utility.returnFormat(
                message_type='success_msg',
                data=UserSerializer(user).data,
                query='fetch_query',
                http_status_code=status.HTTP_200_OK
            )
        return Utility.returnFormat(
                message_type='error_msg',
                data=[],
                query='internal_error',
                http_status_code=status.HTTP_400_BAD_REQUEST
            )
    