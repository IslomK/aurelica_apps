from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Order, OrderDetail, Invoice
from api.serializers import ProductCreateSerializer
from core.exceptions import BadRequest, NotFoundError


class OrderView(APIView):
    serializer = ProductCreateSerializer

    def post(self, request):
        serializer = self.serializer(data=request.data)

        if not serializer.is_valid():
            raise BadRequest(serializer.errors)

        quantity = serializer.validated_data.get('quantity')

        with transaction.atomic():
            try:
                order = Order(customer_id=serializer.validated_data.get('customer_id'))
                order.save()

                order_detail = OrderDetail(
                    quantity=quantity,
                    product_id=serializer.validated_data.get('product_id'),
                    order_id=order.id
                )
                order_detail.save()

                invoice = Invoice(
                    order_id=order.id,
                    amount=(quantity * order_detail.product.price)
                )

                invoice.save()
            except Exception as ex:
                raise BadRequest(ex)

        return Response(data={
            "status": "SUCCESS",
            "invoice_number": invoice.id
        })


class OrderDetailView(APIView):
    def get(self, request):
        order_id = request.GET.get('order_id', None)

        if not order_id:
            raise BadRequest("order_id - param required")

        try:
            order = Order.objects.get(id=order_id)
        except ObjectDoesNotExist as ex:
            raise NotFoundError("No order found with this id - {}".format(order_id))

        products = []
        for order_detail in order.orderdetail_set.all():
            products.append({
                "name": order_detail.product.name,
                "id": order_detail.id,
                "quantity": order_detail.quantity
            })

        return Response(data={
            "id": order.id,
            "customer_id": order.customer_id,
            "products": products
        })

