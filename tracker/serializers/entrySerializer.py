from rest_framework import serializers
from ..models import Category, Entry
from .categorySerializer import CategorySerializer

class EntrySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    category_name = serializers.CharField(source='category.name', read_only=True)


    class Meta:
        model = Entry
        fields = ['id', 'category', 'category_id', 'amount', 'note', 'date', 'type', 'category_name']