from rest_framework.views import APIView
from ..serializers import UserSerializer
from budget_tracker.utility import Utility

class UserDetailView(APIView):
    def post(self, request):
        serializer = UserSerializer(request.user)
        return Utility.returnFormat(
            message_type='success_msg',
            data=serializer.data,
            query='login_query',
            http_status_code=200
        )