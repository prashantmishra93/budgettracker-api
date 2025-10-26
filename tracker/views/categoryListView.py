from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Category
from ..serializers import CategorySerializer
from budget_tracker.utility import Utility
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from math import ceil

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
        perPage = int(request.data.get('per_page', 10))
        page = int(request.data.get('page', 1))

        qs = Category.objects.filter(user=request.user).order_by('-id')

        paginator = Paginator(qs, perPage)
        try:
            entries = paginator.page(page)
        except PageNotAnInteger:
            entries = paginator.page(1)
        except EmptyPage:
            entries = paginator.page(paginator.num_pages)
        serializer = CategorySerializer(entries, many=True)
        last_page = ceil(qs.count() / perPage)
        filterData = {
            "entries": serializer.data,
            "total_items": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": entries.number,
            "per_page": perPage,
            "last_page": last_page,
        }
        return Utility.returnFormat(
                message_type='success_msg',
                data=filterData,
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

class GetCategoryByIdView(APIView):
    def post(self, request):
        category_id = request.data.get('id')
        if not category_id:
            return Utility.returnFormat(
                message_type='error_msg',
                data=[],
                query='validation_error',
                http_status_code=status.HTTP_400_BAD_REQUEST
            )
        
        data = Category.objects.get(id=category_id)
        serializer = CategorySerializer(data)
        return Utility.returnFormat(
            message_type='success_msg',
            data=serializer.data,
            query='fetch_query',
            http_status_code=status.HTTP_200_OK
        )

class UpdateCategoryView(APIView):
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
        except Category.DoesNotExist:
            return Utility.returnFormat(
                message_type='error_msg',
                data=[],
                query='not_found',
                http_status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Utility.returnFormat(
                message_type='success_msg',
                data=serializer.data,
                query='update_query',
                http_status_code=status.HTTP_200_OK
            )
        
        return Utility.returnFormat(
            message_type='error_msg',
            data=serializer.errors,
            query='validation_error',
            http_status_code=status.HTTP_400_BAD_REQUEST
        )