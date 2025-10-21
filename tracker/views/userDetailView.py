from rest_framework.views import APIView
from ..serializers import UserSerializer
from rest_framework import status, permissions
from budget_tracker.utility import Utility
from django.contrib.auth.models import User

class UserDetailView(APIView):
    def post(self, request):
        serializer = UserSerializer(request.user)
        return Utility.returnFormat(
            message_type='success_msg',
            data=serializer.data,
            query='fetch_query',
            http_status_code=200
        )
        

class AllUserView(APIView):
    authentication_classes = []  # diabled all authentication and disables JWT validation
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Utility.returnFormat(
            message_type='success_msg',
            data=serializer.data,
            query='fetch_query',
            http_status_code=200
        )