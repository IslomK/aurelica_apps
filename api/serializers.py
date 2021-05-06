from rest_framework import serializers

from api.models import Invoice, Order, Customer, Category, Product, Payment


class InvoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField(required=True)
    product_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)


class PaymentCreateSerializer(serializers.Serializer):
    invoice_id = serializers.IntegerField(required=True)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
