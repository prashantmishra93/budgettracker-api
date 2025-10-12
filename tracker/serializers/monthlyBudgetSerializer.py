from rest_framework import serializers
from ..models import MonthlyBudget

class MonthlyBudgetSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    class Meta:
        model = MonthlyBudget
        fields = ['id', 'user', 'year', 'month', 'amount']