from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Entry, MonthlyBudget
from django.db.models import Sum
from datetime import date

# Entries summary
class EntrySummaryView(APIView):
    def post(self, request):
        year = request.query_params.get('year', date.today().year)
        month = request.query_params.get('month', date.today().month)

        entries = Entry.objects.filter(date__year=year, date__month=month)
        income = entries.filter(category__type='income').aggregate(total=Sum('amount'))['total'] or 0
        expenses = entries.filter(category__type='expense').aggregate(total=Sum('amount'))['total'] or 0
        balance = income - expenses

        try:
            budget = MonthlyBudget.objects.get(year=year, month=month).amount
        except MonthlyBudget.DoesNotExist:
            budget = None

        return Response({
            'year': int(year),
            'month': int(month),
            'income': float(income),
            'expenses': float(expenses),
            'balance': float(balance),
            'budget': float(budget) if budget is not None else None,
        })
