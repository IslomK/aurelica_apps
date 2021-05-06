from django.contrib import admin

from api.models import Invoice, Payment, Order, OrderDetail, Customer, Product, Category

admin.site.register(Invoice)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Category)