from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import ProductoForm
from .models import Producto
from .models import TipoProducto
from datetime import datetime
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse



def cerrar_sesion(request):
    logout(request)
    return redirect('login')

def index_view(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
          
            return redirect('home')  
        else:
           
            pass

    return render(request, 'registration/login.html')


def registro_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya está en uso.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'El correo electrónico ya está registrado.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user = authenticate(username=username, password=password1)
                if user is not None:
                    login(request, user)
                    return redirect('login') 
        else:
            messages.error(request, 'Las contraseñas no coinciden.')

    return render(request, 'registration/registro.html')

def index( request ):
    return render(request, 'index.html')

def base( request ):
    return render(request, 'base.html')

@login_required
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/listar_productos.html', {'productos': productos})

@login_required
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})

from datetime import datetime
@login_required
def registrar_producto(request):
    tipos = TipoProducto.objects.all()

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()

    hoy = datetime.today().strftime('%Y-%m-%d')

    return render(request, 'productos/registrar_producto.html', {'form': form, 'tipos': tipos, 'hoy': hoy})
def modificar_producto(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    tipos = TipoProducto.objects.all()
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
        
    return render(request, 'productos/modificar_producto.html', {'form': form, 'tipos': tipos})


def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')

    return render(request, 'productos/eliminar_productos.html', {'producto': producto})

#JuanJo

def buscar_productos(request):
    if request.method == 'GET':
        consulta = request.GET.get('consulta')
        resultados = Producto.objects.filter(
            Q(nombre__icontains=consulta) |  
            Q(codigo_barras__icontains=consulta)  
            
        )

    return render(request, 'productos/buscador.html', {'resultados': resultados})


def alertas_bajo_inventario(request):
    if request.method == 'GET':
        
        productos_inventario_bajo = Producto.objects.filter(
            cantidad_inventario__lte=10
        )

      
        fecha_actual = timezone.now()
        fecha_limite = fecha_actual + timezone.timedelta(days=3)
        productos_proximos_a_vencer = Producto.objects.filter(
            Q(fecha_caducidad__gte=fecha_actual) & Q(fecha_caducidad__lte=fecha_limite)
        )

    return render(request, 'productos/alertas.html', {
        'productos_inventario_bajo': productos_inventario_bajo,
        'productos_proximos_a_vencer': productos_proximos_a_vencer,
    })


from django.shortcuts import render
from .models import Producto

def venta(request):
    productos = Producto.objects.all()
    return render(request, 'venta/venta.html', {'productos': productos})

from django.shortcuts import render, redirect
from .models import Venta, Transaccion
from .forms import VentaForm

def listar_ventas(request):
    ventas = Venta.objects.all()

    listadoVentas = []

    for venta in ventas:

        productos = json.loads(venta.productos)
        listado_productos = []

        for p in productos:

            listado_productos.append({

                "nombre": p["nombre"],
                "cantidad": p["cantidad"]

            })

        listadoVentas.append({

            "id": venta.id_venta,
            "fecha": venta.fecha_venta,
            "estado": venta.finalizada,
            "total": venta.total,
            "productos": listado_productos

        })

    return render(request, 'venta/listar_ventas.html', {'ventas': listadoVentas})

@csrf_exempt
def crear_venta(request):
    
    datos = json.loads(request.body)

    productos = json.loads(datos["productos"])

    Venta.objects.create(

        finalizada = True,
        total = datos["total"],
        productos = datos["productos"]

    )

    for i in productos:

        prd = Producto.objects.get(id_producto = i["id"])
        prd.cantidad_inventario -= i["cantidad"]
        prd.save()

    return JsonResponse({"mensaje": "Exito"})
