from rest_framework.views import APIView
from rest_framework import status
from ..models import Entry
from ..serializers import EntrySerializer
from budget_tracker.utility import Utility
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from math import ceil


class EntryListView(APIView):
    def post(self, request):
        perPage = int(request.data.get('per_page', 10))
        page = int(request.data.get('page', 1))
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        # Filter entries for logged-in user
        qs = Entry.objects.filter(user=request.user)

        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        paginator = Paginator(qs, perPage)
        try:
            entries = paginator.page(page)
        except PageNotAnInteger:
            entries = paginator.page(1)
        except EmptyPage:
            entries = paginator.page(paginator.num_pages)

        serializer = EntrySerializer(entries, many=True)
        
        last_page = ceil(qs.count() / perPage)

        data = {
            "entries": serializer.data,
            "total_items": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": entries.number,
            "per_page": perPage,
            "last_page": last_page,
        }
        return Utility.returnFormat(
            message_type='success_msg',
            data=data,
            query='fetch_query',
            http_status_code=status.HTTP_200_OK
        )
