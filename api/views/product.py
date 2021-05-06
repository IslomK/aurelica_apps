from django.core.exceptions import ObjectDoesNotExist, BadRequest
from django.db import DatabaseError
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Product
from api.serializers import ProductSerializer
from core.exceptions import NotFoundError


class ProductListView(APIView):
    serializer = ProductSerializer

    def get(self, request):

        try:
            products = Product.objects.all()
        except DatabaseError as ex:
            raise ex

        serializer = self.serializer(products, many=True)

        return Response(data={
            "data": serializer.data
        })


class ProductDetailView(ProductListView):
    def get(self, request):
        product_id = request.GET.get('product_id', None)

        if not product_id:
            raise BadRequest("product_id - param required")

        try:
            product = Product.objects.get(id=product_id)
        except ObjectDoesNotExist as ex:
            raise NotFoundError("No product found with id - {}".format(product_id))

        serializer = self.serializer(product.category)

        return Response(data=serializer.data)