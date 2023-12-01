const listaProductosVenta = []

document.addEventListener('DOMContentLoaded', function() {
    const buscador = document.getElementById('buscador');
    const listaProductos = document.getElementById('lista-productos');
    const productos = document.querySelectorAll(".producto")
    const editarModalBtn = document.getElementById('editar-modal');

    const modalNombre = document.getElementById('modal-nombre');
    const modalPrecio = document.getElementById('modal-precio');
    const modalCantidad = document.getElementById('modal-cantidad');
    const valorPago = document.getElementById("pago")
    const agregarModalBtn = document.getElementById('agregar-modal');

    const realizarVenta = document.getElementById("finalizar")

    const totalTodo = document.getElementById("transaccion")
    const prds = document.getElementById("total")

    let productoEditado = null;

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

    let id = 0

    productos.forEach(prd => {

        prd.addEventListener("click", (e) => {

            const nombre = prd.textContent.split(' - ')[0];
            const precio = parseFloat(prd.dataset.precio);

            id = e.target.attributes[1].value
            modalNombre.textContent = nombre;
            modalPrecio.textContent = `$${precio.toFixed(2)}`;
            modalCantidad.value = '1';
            editarModalBtn.style.display = 'none';
            agregarModalBtn.style.display = 'block';

            const modal = document.getElementById('modal');
            modal.style.display = 'block';

        })

    })

    function borrar(id){

        const lista = JSON.parse(localStorage.getItem("productos"))

        const nuevaLista = lista.slice(id, 1)
    
        console.log(id)

    }

    agregarModalBtn.addEventListener('click', () => {
        const cantidad = parseInt(modalCantidad.value);

        if (cantidad > 0) {
            modal.style.display = 'none';
            modalCantidad.value = '1';

            const nombreConvertido = modalNombre.textContent.trim()
            const precioConvertido = modalPrecio.textContent.split("$")

            listaProductosVenta.push({

                id: id,
                nombre: nombreConvertido,
                cantidad: cantidad,
                precio: parseFloat(precioConvertido[1]) * cantidad

            })

            localStorage.setItem("productos", JSON.stringify(listaProductosVenta))

            let productos = JSON.parse(localStorage.getItem("productos"))

            let total = 0
            
            prds.innerHTML = "<p> </p>"

            for (let i in productos){

                prds.innerHTML += `
                
                    <span> Nombre:  ${productos[i].nombre} - Cantidad: ${productos[i].cantidad} </span> 
                    <button> X </button> <br>
                
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

        e.preventDefault()

        const productosLocalStorage = JSON.parse(localStorage.getItem("productos"))

        let totalVenta = 0

        for (let i of productosLocalStorage){

            totalVenta += i.precio

        }

        if(parseInt(valorPago.value) >= totalVenta){

            const peticion = await fetch("http://localhost:8000/crear_venta/", {

                method: 'POST',
                body: JSON.stringify({

                    total: totalVenta,
                    productos: localStorage.getItem("productos")

                }),
                headers: {"content-type": "application/json"}

            })

            await peticion.json()

            alert(`Cambio: ${parseInt(valorPago.value) - totalVenta}`);


            localStorage.removeItem("productos")

        }else{

            alert(`Faltan: ${totalVenta - parseInt(valorPago.value)}`);

            localStorage.removeItem("productos")

        }

    })


});
