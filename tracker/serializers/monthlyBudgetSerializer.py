from rest_framework import serializers
from ..models import MonthlyBudget

class MonthlyBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyBudget
        fields = ['id', 'year', 'month', 'amount']