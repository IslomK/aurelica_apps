import datetime

from django.db import DatabaseError
from rest_framework.decorators import api_view
from django.db.models import F, Count, Sum, Avg
from rest_framework.response import Response

from api.models import Invoice, Order, Customer, Product, OrderDetail
from api.serializers import InvoicesSerializer, OrderSerializer, CustomerSerializer


@api_view(['GET'])
def expired_invoices(request):

    try:
        invoices = Invoice.objects.filter(
            issued__gt=F('due')
        )
    except DatabaseError as ex:
        raise ex

    serializer = InvoicesSerializer(invoices, many=True)

    return Response(data={"data": serializer.data})


@api_view(['GET'])
def order_without_details(request):
    try:
        orders = Order.objects.filter(
            created_at__lt=datetime.date(2016, 9, 6),
            orderdetail__isnull=True
        )
    except DatabaseError as ex:
        raise ex

    serializer = OrderSerializer(orders, many=True)

    return Response(data={"data": serializer.data})


@api_view(['GET'])
def wrong_date_invoices(request):
    try:
        invoices = Invoice.objects.filter(
            issued__lt=F('order_id__created_at')
        )
    except DatabaseError as ex:
        raise ex

    resp = []
    for invoice in invoices:
        resp.append({
            "id": invoice.id,
            "issued": invoice.issued,
            "order_id": invoice.order_id,
            "order_created_at": invoice.order.created_at
        })

    return Response(data={
        "data": resp
    })


@api_view(['GET'])
def customers_without_orders(request):
    try:
        customers = Customer.objects.exclude(
            order__created_at__gt=datetime.datetime(2016, 1, 1)
        )
    except DatabaseError as ex:
        raise ex

    serializer = CustomerSerializer(customers, many=True)

    return Response(data={
        "data": serializer.data
    })


@api_view(['GET'])
def customers_last_orders(request):
    try:
        customers = Customer.objects.exclude(
            order__isnull=True
        )
    except DatabaseError as ex:
        raise ex

    resp = []
    for customer in customers:
        resp.append({
            "name": customer.name,
            "id": customer.id,
            "last_order_date": customer.order_set.order_by('-created_at').first().created_at
        })

    return Response(data={
        "data": resp
    })


@api_view(['GET'])
def overpaid_invoices(request):
    try:
        invoices = Invoice.objects.annotate(
            payment_count=Count('payment'),
            total_amount=Sum('payment__amount')
        ).filter(
            payment_count__gt=1
        )
    except DatabaseError as ex:
        raise ex

    resp = []
    for invoice in invoices:
        resp.append({
            "id": invoice.id,
            "reimburse_amount": invoice.total_amount - invoice.amount
        })

    return Response(data={
        "data": resp
    })


@api_view(['GET'])
def high_demand_products(request):
    try:
        products = Product.objects.annotate(
            total_count=Sum('orderdetail__quantity'),
        ).filter(
            total_count__gte=10,
        )
    except DatabaseError as ex:
        raise ex

    resp = []
    for product in products:
        resp.append({
            "total_count": product.total_count,
            "product_code": product.name
        })

    return Response(data={
        "data": resp
    })


@api_view(['GET'])
def bulk_products(request):
    try:
        products = Product.objects.annotate(
            avg_count=Avg('orderdetail__quantity')
        ).filter(
            avg_count__gte=8
        )
    except DatabaseError as ex:
        raise ex

    resp = []
    for product in products:
        resp.append({
            "product": product.name,
            "price": product.price
        })

    return Response(data={
        "data": resp
    })


@api_view(['GET'])
def number_of_products_in_year(request):
    try:
        customers = Customer.objects.values('country').annotate(
                order_count=Count('order')
            ).filter(
                order__created_at__range=[datetime.datetime(2016, 1, 1), datetime.datetime(2017, 1, 1)],
                order_count__gte=1
            )
    except DatabaseError as ex:
        raise ex

    resp = []
    for customer in customers:
        resp.append({
            "country": customer.get('country'),
            "order_count": customer.get('order_count')
        })

    return Response(data={
        "data": resp
    })


@api_view(['GET'])
def orders_without_invoices(request):
    try:
        results = OrderDetail.objects.values('order_id', 'product__price').annotate(
            total_count=Sum('quantity'),
        ).filter(
            order__invoice__isnull=True,
        )
    except DatabaseError as ex:
        raise ex

    resp = []
    for result in results:
        resp.append({
            "order_id": result.get('order_id'),
            "total_price": (result.get('product__price') * result.get('total_count'))
        })

    return Response(data={
        "data": resp
    })