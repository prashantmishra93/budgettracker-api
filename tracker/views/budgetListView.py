from rest_framework.views import APIView
from rest_framework import status
from ..serializers import MonthlyBudgetSerializer
from budget_tracker.utility import Utility

# Budgets
class BudgetListView(APIView):
    def post(self, request):
        serializer = MonthlyBudgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
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

