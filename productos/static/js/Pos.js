const listaProductosVenta = [];

document.addEventListener('DOMContentLoaded', function() {
    const buscador = document.getElementById('buscador');
    const listaProductos = document.getElementById('lista-productos');
    const productos = document.querySelectorAll(".producto");
    const editarModalBtn = document.getElementById('editar-modal');

    const modalNombre = document.getElementById('modal-nombre');
    const modalPrecio = document.getElementById('modal-precio');
    const modalCantidad = document.getElementById('modal-cantidad');
    const valorPago = document.getElementById("pago");
    const agregarModalBtn = document.getElementById('agregar-modal');

    const realizarVenta = document.getElementById("finalizar");

    const totalTodo = document.getElementById("transaccion");
    const prds = document.getElementById("total");

    buscador.addEventListener('input', function() {
        const filtro = this.value.toLowerCase();

        for (const producto of listaProductos.children) {
            const nombre = producto.textContent.toLowerCase();

            if (nombre.includes(filtro)) {
                producto.style.display = 'block';
            } else {
                producto.style.display = 'none';
            }
        }
    });

    productos.forEach(prd => {
        prd.addEventListener("click", () => {
            const nombre = prd.textContent.split(' - ')[0];
            const precio = parseFloat(prd.dataset.precio);

            modalNombre.textContent = nombre;
            modalPrecio.textContent = `$${precio.toFixed(2)}`;
            modalCantidad.value = '1';
            editarModalBtn.style.display = 'none';
            agregarModalBtn.style.display = 'block';

            const modal = document.getElementById('modal');
            modal.style.display = 'block';
        });
    });

    agregarModalBtn.addEventListener('click', () => {
        const cantidad = parseInt(modalCantidad.value);

        if (cantidad > 0) {
            modal.style.display = 'none';
            modalCantidad.value = '1';

            const nombreConvertido = modalNombre.textContent.trim();
            const precioConvertido = modalPrecio.textContent.split("$");

            listaProductosVenta.push({
                nombre: nombreConvertido,
                cantidad: cantidad,
                precio: parseFloat(precioConvertido[1]) * cantidad
            });

            localStorage.setItem("productos", JSON.stringify(listaProductosVenta));

            let productos = JSON.parse(localStorage.getItem("productos"));

            let total = 0;

            prds.innerHTML = "<p> </p>";

            for (let i in productos) {
                prds.innerHTML += `
                    <span> Nombre: ${productos[i].nombre} - Cantidad: ${productos[i].cantidad} </span>
                    <button class="eliminar-producto" data-id="${i}"> X </button> <br>
                `
                total += productos[i].precio
            }

            totalTodo.textContent = `Total: $${total.toFixed(2)}`;
        }
    });

    prds.addEventListener('click', (e) => {
        if (e.target.classList.contains('eliminar-producto')) {
            const index = parseInt(e.target.dataset.id);
            listaProductosVenta.splice(index, 1);

            localStorage.setItem("productos", JSON.stringify(listaProductosVenta));

            let productos = JSON.parse(localStorage.getItem("productos"));

            let total = 0;

            prds.innerHTML = "<p> </p>";

            for (let i in productos) {
                prds.innerHTML += `
                    <span> Nombre: ${productos[i].nombre} - Cantidad: ${productos[i].cantidad} </span>
                    <button class="eliminar-producto" data-id="${i}"> X </button> <br>
                `
                total += productos[i].precio
            }

            totalTodo.textContent = `Total: $${total.toFixed(2)}`;
        }
    });

    const cantidadSelector = document.querySelector('.cantidad-selector');
    cantidadSelector.addEventListener('click', function(event) {
        if (event.target.classList.contains('cantidad-btn')) {
            const buttonValue = event.target.textContent;

            // Limpiar el campo de cantidad antes de agregar el nuevo valor
            const modalCantidad = document.getElementById('modal-cantidad');
            modalCantidad.value = buttonValue;
        }
    });

    const closeModal = document.querySelector('.close');
    closeModal.addEventListener('click', function() {
        const modal = document.getElementById('modal');
        modal.style.display = 'none';
    });

    realizarVenta.addEventListener("click", async (e) => {
        e.preventDefault();
    
        const productosLocalStorage = JSON.parse(localStorage.getItem("productos"));
        const totalVenta = productosLocalStorage.reduce((total, producto) => total + producto.precio, 0);
    
        if (parseInt(valorPago.value) >= totalVenta) {
            const formData = new FormData();
            formData.append('total', totalVenta);
            formData.append('productos', JSON.stringify(productosLocalStorage));
    
            const peticion = await fetch("http://localhost:8000/crear_venta/", {
                method: 'POST',
                body: formData,
            });
    
            await peticion.json();
    
            alert(`Cambio: ${parseInt(valorPago.value) - totalVenta}`);
            localStorage.removeItem("productos");
        } else {
            alert(`Faltan: ${totalVenta - parseInt(valorPago.value)}`);
            localStorage.removeItem("productos");
        }
    });
});
