from django.urls import path
from api.views.category import CategoryListView, ProductCategoryView
from api.views.order import OrderView, OrderDetailView
from api.views.payment import PaymentView
from api.views.product import ProductListView, ProductDetailView

urlpatterns = [
    path('order/', OrderView.as_view(), name='order'),
    path('order/details/', OrderDetailView.as_view(), name='order_detail'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('payment/details/', PaymentView.as_view(), name='payment'),
    path('payment/details/', OrderDetailView.as_view(), name='order'),
    path('category/list/', CategoryListView.as_view(), name='category_list'),
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path(r'category/', ProductCategoryView.as_view(), name='product_category'),
    path(r'product/details/', ProductDetailView.as_view(), name='product_list'),
]