from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Entry
from ..serializers import EntrySerializer


# Entries
class EntryListView(APIView):
    def get(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        qs = Entry.objects.all()
        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        serializer = EntrySerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)