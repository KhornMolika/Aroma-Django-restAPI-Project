from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Image)
admin.site.register(ImageType)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductDetail)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(QRCode)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BlogCategory)
admin.site.register(Blog)
admin.site.register(BlogDetail)

admin.site.register(AccessToken)
