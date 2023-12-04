from django.urls import path
from .views import listar_productos, registrar_producto, informe_ventas, descargar_excel,index, modificar_producto, base, eliminar_producto, buscar_productos
from . import views
from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import venta, listar_ventas


urlpatterns = [
    path('', views.login_view, name='login'),  
    path('base/', base, name='hogar'),
    path('inicio/', index, name='home'),  
    path('listar/', listar_productos, name='listar_productos'),
    path('registrar/', views.registrar_producto, name='registrar_producto'),
    path('modificar/<int:id>/', login_required(modificar_producto), name='modificar_producto'),
    path('eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('registro/', views.registro_view, name='registro'),
    path('buscar/', buscar_productos, name='buscar_productos'),
    path('alertas/', views.alertas_bajo_inventario, name='alertas_productos'),
    path('detalle/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('productos_bajo_inventario/', views.alertas_bajo_inventario, name='productos_bajo_inventario'),
    path('venta/', views.venta, name='venta'),
    path('crear_venta/', views.crear_venta, name='crear_venta'),
    path('listar_ventas/', listar_ventas, name='listar_ventas'),
    path('informe_ventas/', informe_ventas, name='informe_ventas'),
    path('descargar_excel/', descargar_excel, name='descargar_excel'),
    
]



