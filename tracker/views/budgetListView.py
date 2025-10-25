from rest_framework.views import APIView
from rest_framework import status
from ..serializers import MonthlyBudgetSerializer
from budget_tracker.utility import Utility
from ..models import MonthlyBudget

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

class DeleteBudgetView(APIView):
    def post(self, request):
        category_id = request.data.get('id')

        if not category_id:
            return Utility.returnFormat(
                message_type='error_msg',
                data=[],
                query='validation_error',
                http_status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            category = MonthlyBudget.objects.get(id=category_id)
            category.delete()
            return Utility.returnFormat(
                message_type='success_msg',
                data=[],
                query='delete_query',
                http_status_code=status.HTTP_200_OK
            )
        except MonthlyBudget.DoesNotExist:
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