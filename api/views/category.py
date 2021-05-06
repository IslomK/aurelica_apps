from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Category, Product
from api.serializers import CategorySerializer
from core.exceptions import BadRequest, NotFoundError


class CategoryListView(APIView):
    serializer = CategorySerializer

    def get(self, request):

        try:
            categories = Category.objects.all()
        except DatabaseError as ex:
            raise ex

        serializer = self.serializer(categories, many=True)

        return Response(data={
            "data": serializer.data
        })


class ProductCategoryView(CategoryListView):
    def get(self, request):
        product_id = request.GET.get('product_id', None)

        if not product_id:
            raise BadRequest("product_id - param required")

        try:
            product = Product.objects.get(id=product_id)
        except ObjectDoesNotExist as ex:
            raise NotFoundError("No product found with this id - {}".format(product_id))

        serializer = self.serializer(product.category)

        return Response(data=serializer.data)