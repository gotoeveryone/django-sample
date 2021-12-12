from django.contrib import admin
from api.models import Product, Tag, PurchaseHistory


admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(PurchaseHistory)
