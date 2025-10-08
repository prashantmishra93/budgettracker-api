from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import MonthlyBudget
from ..serializers import MonthlyBudgetSerializer

# Get all budgets
class GetBudgetsView(APIView):
    def get(self, request):
        budgets = MonthlyBudget.objects.all().order_by('-year', '-month')
        serializer = MonthlyBudgetSerializer(budgets, many=True)
        return Response(serializer.data)