from django import forms
from .models import Producto, Venta, Transaccion
from datetime import date

class ProductoForm(forms.ModelForm):
    fecha_caducidad = forms.DateField()

    class Meta:
        model = Producto
        fields = ['nombre', 'codigo_barras', 'precio_costo', 'precio_venta', 'precio_mayor', 'fecha_caducidad', 'cantidad_inventario', 'inventario_minimo', 'tipo']

    def clean_fecha_caducidad(self):
        fecha_caducidad = self.cleaned_data.get('fecha_caducidad')
        if fecha_caducidad and fecha_caducidad < date.today():
            error_message = "No puedes seleccionar una fecha anterior a la actual."
            error_style = 'color: red; font-weight: bold;'
            raise forms.ValidationError(f'<span style="{error_style}">{error_message}</span>', code='invalid')
        return fecha_caducidad

class ActualizarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'codigo_barras', 'precio_costo', 'precio_venta', 'precio_mayor', 'fecha_caducidad', 'cantidad_inventario', 'inventario_minimo', 'tipo']

class BuscadorProductos(forms.Form):
    consulta = forms.CharField(label='Buscar')
from django import forms
from .models import Transaccion, Venta

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['id_producto', 'cantidad']
        
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['finalizada']