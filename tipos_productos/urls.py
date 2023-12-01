from django.urls import path
from . import views

urlpatterns = [

    path('agregar/', views.agregar_tipo_producto, name='agregar_tipo_producto'),
    path('mostrar_tipos/', views.mostrar_tipos_productos, name='mostrar_tipos_productos'),
    path('eliminar/<int:tipo_producto_id>/', views.eliminar_tipo_producto, name='eliminar_tipo_producto'),
    path('modificar/<int:tipo_producto_id>/', views.modificar_tipo_producto, name='modificar_tipo_producto'),

]