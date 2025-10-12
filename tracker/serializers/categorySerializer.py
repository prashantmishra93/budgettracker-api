from rest_framework import serializers
from ..models import Category


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    class Meta:
        model = Category
        fields = ['id', 'user', 'name', 'type']