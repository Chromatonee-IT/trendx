from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(customer)
admin.site.register(products)
admin.site.register(orders)
admin.site.register(address)
admin.site.register(category)
admin.site.register(subcategory)
admin.site.register(product_variants)
admin.site.register(product_metas)
admin.site.register(product_images)
admin.site.register(reviews)
admin.site.register(home_offers)
admin.site.register(discount)
admin.site.register(discount_type)
