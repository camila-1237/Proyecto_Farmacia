from django.contrib import admin

from .models  import Producto
from. models import Venta
from. models import Transaccion


admin.site.register(Producto)
admin.site.register(Venta)
admin.site.register(Transaccion)