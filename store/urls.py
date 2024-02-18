from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('cart/',views.cart, name='cart'),
    path('checkout/',views.checkout, name='checkout'),
    path('all_products/',views.all_products, name='all_products'),
    path('product_single/<int:id>', views.product_single, name='product_single'),
    path('all_stores/',views.all_stores, name='all_stores'),
    path('login/',views.login_user, name='login'),
    path('register/',views.register_user, name='register'),
    path('logout/',views.logout_user, name='logout'),
    path('forgotpass/',views.forgotpass, name='forgotpass'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('oders/',views.orders_user,name='orders'),
    path('address/',views.address_user,name='address'),
    path('payment_method/',views.payment_method,name='payment_method'),
    path('my_reviews/',views.my_reviews,name='my_reviews'),
    path('my_favourites/',views.my_favourites,name='my_favourites'),
    # path('<str:category_name>/',views.category_detail,name='category_detail'),
    # path('<str:category_name>/<str:subcategory_name>',views.subcategory_detail,name='subcategory_detail'),

]
