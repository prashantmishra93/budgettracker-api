from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import MonthlyBudget
from ..serializers import MonthlyBudgetSerializer
from budget_tracker.utility import Utility
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from math import ceil

# Get all budgets
class GetBudgetsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        perPage = int(request.query_params.get('per_page', 10))
        page = int(request.query_params.get('page', 1))

        qs = MonthlyBudget.objects.filter(user=request.user).order_by('-id')

        paginator = Paginator(qs, perPage)
        try:
            entries = paginator.page(page)
        except PageNotAnInteger:
            entries = paginator.page(1)
        except EmptyPage:
            entries = paginator.page(paginator.num_pages)

        serializer = MonthlyBudgetSerializer(entries, many=True)
        last_page = ceil(qs.count() / perPage)
        filterData = {
            "entries": serializer.data,
            "total_items": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": entries.number,
            "per_page": perPage,
            "last_page": last_page,
        }
        return Utility.returnFormat(
            message_type='success_msg',
            data=filterData,
            query='store_query',
            http_status_code=status.HTTP_201_CREATED
        )