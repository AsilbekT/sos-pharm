from django.contrib import admin
from mobile.models import Snippet, Aptekalar, Sotuvchilar,Dorilar, Order, OrderItem, OrderQarz, OrderQarzItem
# Register your models here.

admin.site.register(Snippet)
admin.site.register(Aptekalar)
admin.site.register(Sotuvchilar)
admin.site.register(Dorilar)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderQarz)
admin.site.register(OrderQarzItem)


