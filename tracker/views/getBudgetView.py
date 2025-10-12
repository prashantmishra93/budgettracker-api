from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import MonthlyBudget
from ..serializers import MonthlyBudgetSerializer
from budget_tracker.utility import Utility

# Get all budgets
class GetBudgetsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        budgets = MonthlyBudget.objects.all().order_by('-year', '-month')
        serializer = MonthlyBudgetSerializer(budgets, many=True)
        return Utility.returnFormat(
            message_type='success_msg',
            data=serializer.data,
            query='fetch_query',
            http_status_code=status.HTTP_200_OK
        )