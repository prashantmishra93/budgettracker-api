from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import EntrySerializer
from budget_tracker.utility import Utility

class EntryCreateView(APIView):
    def post(self, request):
        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # assuming entries are tied to logged-in user
            return Utility.returnFormat(
                message_type='success_msg',
                data=serializer.data,
                query='store_query',
                http_status_code=status.HTTP_201_CREATED
            )
        return Utility.returnFormat(
            message_type='error_msg',
            data=serializer.errors,
            query='validation_error',
            http_status_code=status.HTTP_400_BAD_REQUEST
        )