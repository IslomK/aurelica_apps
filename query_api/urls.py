from django.urls import path
from query_api.views import *

urlpatterns = [
    path('expired_invoices/', expired_invoices, name='expired_invoices'),
    path('wrong_date_invoices/', wrong_date_invoices, name='wrong_date_invoices'),
    path('order_without_details/', order_without_details, name='order_without_details'),
    path('customers_without_orders/', customers_without_orders, name='customers_without_orders'),
    path('customers_last_orders/', customers_last_orders, name='customers_last_orders'),
    path('overpaid_invoices/', overpaid_invoices, name='overpaid_invoices'),
    path('high_demand_products/', high_demand_products, name='high_demand_products'),
    path('bulk_products/', bulk_products, name='bulk_products'),
    path('number_of_products_in_year/', number_of_products_in_year, name='number_of_products_in_year'),
    path('orders_without_invoices/', orders_without_invoices, name='orders_without_invoices'),
]