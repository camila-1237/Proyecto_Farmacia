from django.db import models
from tipos_productos.models import TipoProducto

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    codigo_barras = models.CharField(max_length=13, unique=True)
    precio_costo = models.DecimalField(max_digits=10, decimal_places=3)  
    precio_venta = models.DecimalField(max_digits=10, decimal_places=3) 
    precio_mayor = models.DecimalField(max_digits=10, decimal_places=2) 
    fecha_caducidad = models.DateTimeField()
    cantidad_inventario = models.DecimalField(max_digits=10, decimal_places=2)
    inventario_minimo = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)  
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)

    def __str__(self):  
        return self.nombre


class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    finalizada = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    productos = models.TextField(default="[]") 

    def calcular_total(self):
        transacciones = self.transaccion_set.all()
        total = sum(transaccion.calcular_subtotal() for transaccion in transacciones)
        self.total = total
        self.save()
        return round(total, 2)

    def __str__(self):
        return f'Venta {self.id_venta}'
class Transaccion(models.Model):
    id_transaccion = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    finalizada = models.BooleanField(default=False)
    
    def calcular_subtotal(self):
        return self.cantidad * self.id_producto.precio_venta

    def detalles_producto_vendido(self):
        return f'{self.id_producto.nombre} - Cantidad: {self.cantidad}'

    def _str_(self):
        return f'Transacción: {self.id_producto.nombre} en Venta {self.id_venta.id_venta}'