from rest_framework.views import APIView
from ..models import Entry, MonthlyBudget
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from rest_framework import status
from budget_tracker.utility import Utility
from datetime import date
import calendar

class EntrySummaryView(APIView):
    def post(self, request):
        year = request.data.get('year') or request.query_params.get('year')

        # If year not provided anywhere, fallback to current year
        if year is None or year == '':
            year = date.today().year
        else:
            year = int(year)
        print(year)
        
        entries = Entry.objects.all()
        
        if year:
            entries = entries.filter(date__year=year)
            
        print(entries)
        allYearBudget = MonthlyBudget.objects.values_list('year', flat=True).distinct().order_by('year')
        available_years = list(allYearBudget)
        entries = (
            entries.annotate(year=ExtractYear('date'), month=ExtractMonth('date'))
            .values('year', 'month', 'category__type')
            .annotate(total=Sum('amount'))
            .order_by('year', 'month')
        )

        # Step 2: Structure income/expense totals
        grouped = {}
        for e in entries:
            year = e['year']
            month = e['month']
            entry_type = e['category__type']
            total = e['total']

            if year not in grouped:
                grouped[year] = {}
            if month not in grouped[year]:
                grouped[year][month] = {'income': 0, 'expenses': 0}

            if entry_type == 'income':
                grouped[year][month]['income'] = total
            elif entry_type == 'expense':
                grouped[year][month]['expenses'] = total

        # Step 3: Fetch all budgets and map them by (year, month)
        budgets = MonthlyBudget.objects.values('year', 'month', 'amount')
        budget_map = {(b['year'], b['month']): b['amount'] for b in budgets}

        # Step 4: Combine everything into a year->months list
        final_result = []
        for year, months_data in grouped.items():
            months_list = []
            for month in range(1, 13):  # Ensure all 12 months are included
                income = float(months_data.get(month, {}).get('income', 0))
                expenses = float(months_data.get(month, {}).get('expenses', 0))
                balance = income - expenses
                budget = float(budget_map.get((year, month), 0)) or None
                month_name = calendar.month_name[month]

                months_list.append({
                    'month': month,
                    'income': income,
                    'expenses': expenses,
                    'balance': balance,
                    'budget': budget,
                    'month_name': month_name,
                })

            final_result.append({
                'year': year,
                'months': months_list
            })

        return Utility.returnFormat(
            message_type='success_msg',
            data=final_result,
            query='fetch_query',
            http_status_code=status.HTTP_200_OK,
            extra=available_years,
        )
