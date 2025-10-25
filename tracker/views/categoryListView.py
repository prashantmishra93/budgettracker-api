from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Category
from ..serializers import CategorySerializer
from budget_tracker.utility import Utility

class CategoryCreateView(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
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

class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        categories = Category.objects.filter(user=request.user)
        serializer = CategorySerializer(categories, many=True)
        return Utility.returnFormat(
                message_type='success_msg',
                data=serializer.data,
                query='fetch_query',
                http_status_code=status.HTTP_200_OK
            )
class DeleteCategoryView(APIView):
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
            category = Category.objects.get(id=category_id)
            category.delete()
            return Utility.returnFormat(
                message_type='success_msg',
                data=[],
                query='delete_query',
                http_status_code=status.HTTP_200_OK
            )
        except Category.DoesNotExist:
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