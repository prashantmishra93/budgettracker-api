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
        category_name = request.data.get('category', '').strip()
        date = request.data.get('date', '').strip()
        amount = request.data.get('amount', '').strip()
        # Filter entries for logged-in user
        qs = Entry.objects.filter(user=request.user)

        if category_name:
            qs = qs.filter(category__name__icontains=category_name)
        if date:
            qs = qs.filter(date=date)
        if amount:
            qs = qs.filter(amount=amount)

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


class DeleteTransactionView(APIView):
    def post(self, request):
        trans_id = request.data.get('id')

        if not trans_id:
            return Utility.returnFormat(
                message_type='error_msg',
                data=[],
                query='validation_error',
                http_status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            category = Entry.objects.get(id=trans_id)
            category.delete()
            return Utility.returnFormat(
                message_type='success_msg',
                data=[],
                query='delete_query',
                http_status_code=status.HTTP_200_OK
            )
        except Entry.DoesNotExist:
            return Utility.returnFormat(
                message_type='error_msg',
                data=[],
                query='validation_error',
                http_status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Utility.returnFormat(
                message_type='error_msg',
                data=[],
                query='validation_error',
                http_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetEntryByIdView(APIView):
    def post(self, request):
        entry_id = request.data.get('id')
        if not entry_id:
            return Utility.returnFormat(
                message_type='error_msg',
                data=[],
                query='validation_error',
                http_status_code=status.HTTP_400_BAD_REQUEST
            )
        
        data = Entry.objects.get(id=entry_id)
        serializer = EntrySerializer(data)
        return Utility.returnFormat(
            message_type='success_msg',
            data=serializer.data,
            query='fetch_query',
            http_status_code=status.HTTP_200_OK
        )

class UpdateEntryView(APIView):
    def post(self, request):
        entry_id = request.data.get('id')

        if not entry_id:
            return Utility.returnFormat(
                message_type='error_msg',
                data=[],
                query='validation_error',
                http_status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            entry = Entry.objects.get(id=entry_id)
        except Entry.DoesNotExist:
            return Utility.returnFormat(
                message_type='error_msg',
                data=[],
                query='not_found',
                http_status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = EntrySerializer(entry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Utility.returnFormat(
                message_type='success_msg',
                data=serializer.data,
                query='update_query',
                http_status_code=status.HTTP_200_OK
            )
        return Utility.returnFormat(
            message_type='error_msg',
            data=serializer.errors,
            query='validation_error',
            http_status_code=status.HTTP_400_BAD_REQUEST
        )