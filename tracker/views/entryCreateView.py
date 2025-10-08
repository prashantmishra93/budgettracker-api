from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import EntrySerializer

class EntryCreateView(APIView):
    def post(self, request):
        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # assuming entries are tied to logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)