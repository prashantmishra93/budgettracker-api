from rest_framework import serializers
from ..models import StockPrice

class StockPriceSerialer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = ['id', 'symbol', 'price', 'fetched_at']