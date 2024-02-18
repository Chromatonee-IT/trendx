from django.urls import path
from . import views

urlpatterns = [
    path('admin_dashboard/',views.dashboard,name='v_dashboard'),
    path('store_details/',views.store_details,name='store_details'),
    path('products/',views.all_products,name='products'),
    path('orders_vendor/',views.all_orders,name='orders_vendor'),
    path('order_details/<int:id>',views.order_details,name='order_details'),
    path('customers/',views.customers,name='customers'),
    path('customer_details/<int:id>',views.customer_details,name='customer_details'),
    path('sales_promotions/',views.sales_promotions,name='sales_promotions'),
    path('coupon_edit/<int:id>',views.coupon_edit,name='coupon_edit'),
    path('coupon_add/',views.coupon_add,name='coupon_add'),
    path('create_invoice/',views.create_invoice,name='create_invoice'),
    path('all_report/',views.all_report,name='all_report'),
    path('help/',views.help,name='help'),
    path('product_add/',views.product_add,name='product_add'),
    path('product_details/<str:id>',views.product_details,name='product_details'),
    path('v_login/',views.v_login,name='v_login'),
    path('vendor_logout/',views.vendor_logout,name='vendor_logout'),
    path('toggle-product/<int:product_id>/', views.toggle_product, name='toggle_product'),
    ]
