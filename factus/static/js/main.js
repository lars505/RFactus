// Variables globales para la factura
let productosEnFactura = [];


function load_data() {
    fetch('/load_data/')
    .then(response => response.json())
    .then(data => {
    
        cargarProductos(data.products);
        cargarTiposIdentificacion(data.document_types);
        cargarMetodosPago(data.payment_methods);
        cargaroMunicipio(data.municipality);
    })
    .catch(error =>{
        console.log("Error al cargar datos");
        console.error(error);
    })
    .finally(() => {
        
    });
           
}


function cargarProductos(productos) {
    const productoSelect = document.getElementById('productoSelect');
    productos.forEach(producto => {
        const option = document.createElement('option');
        option.value = producto.id;
        option.textContent = `${producto.name} ($${producto.price})`;
        productoSelect.appendChild(option);
    });
}

function cargarTiposIdentificacion(tipos) {
    const tipoIdentificacionSelect = document.getElementById('IdentificationDocumentType');
    tipos.forEach(tipo => {
        const option = document.createElement('option');
        option.value = tipo.id;
        option.textContent = tipo.name;
        tipoIdentificacionSelect.appendChild(option);
    });
}

function cargarMetodosPago(metodos) {
    const metodoPagoSelect = document.getElementById('metodoPago');
    metodos.forEach(metodo => {
        const option = document.createElement('option');
        option.value = metodo.code;
        option.textContent = metodo.description;
        metodoPagoSelect.appendChild(option);
    });
}

function cargaroMunicipio(metodos) {
    const metodoPagoSelect = document.getElementById('municipio');
    metodos.forEach(metodo => {
        const option = document.createElement('option');
        option.value = metodo.id;
        option.textContent = `${metodo.name} - ${metodo.department}`;
        metodoPagoSelect.appendChild(option);
    });
}


function agregarProductoAFactura() {
    
    const productoSelect = document.getElementById('productoSelect');
    const cantidadInput = document.getElementById('cantidad');
    // const productos = JSON.parse(localStorage.getItem('productos')) || [];
    
    // const producto = productos.find(p => p.codigo === productoSelect.value);
    // if (!producto) return;

    fetch(`/load_product/${productoSelect.value}`)
    .then(response => response.json())
    .then(data =>  {
       
        const cantidad = parseInt(cantidadInput.value);
        
        if (cantidad <= 0 || cantidad > data.stock) {
            alert('Cantidad no válida o insuficiente stock');
            return;
        }
        
        const productoEnFactura = {
            data,
            iva,
            cantidad,
            subtotal: data.price * cantidad
        };

        // console.log(productoEnFactura)
        productosEnFactura.push(productoEnFactura);
        actualizarTablaFactura();
        calcularTotales();
        // Resetear campos
        productoSelect.value = '';
        cantidadInput.value = '1';
    })



    
}

function actualizarTablaFactura() {
    const tabla = document.getElementById('productosFactura');
    
    if (!tabla) return;

    tabla.innerHTML = productosEnFactura.map(producto => `
        <tr>
            <td>
             <img src="${producto.data.image}" alt="" class="img-thumbnail" style="width: 50px; height: 50px;">
            </td>
            <td>${producto.data.name}</td>
            <td>$${producto.data.price}</td>
            <td>${producto.cantidad}</td>
            <td>$${producto.subtotal}</td>
            <td>
                <button class="btn btn-sm btn-danger" onclick="eliminarProductoDeFactura('${producto.data.id}')">
                    Eliminar
                </button>
            </td>
        </tr>
    `).join('');
}

function eliminarProductoDeFactura(id) {
    console.log('ID recibido:', id);
    console.log('IDs en productosEnFactura:', productosEnFactura.map(producto => producto.data.id));
    
    productosEnFactura = productosEnFactura.filter(producto => String(producto.data.id) !== String(id));

    console.log('Después de eliminar:', productosEnFactura);

    actualizarTablaFactura();
    calcularTotales();
}



function calcularTotales() {
    const subtotal = productosEnFactura.reduce((sum, producto) => sum + producto.subtotal, 0);
    const aplicaIVA = document.getElementById('aplicaIVA').checked;
    const iva = aplicaIVA ? subtotal * 0.15 : 0;
    const total = subtotal + iva;

    document.getElementById('subtotal').textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById('iva').textContent = `$${iva.toFixed(2)}`;
    document.getElementById('total').textContent = `$${total.toFixed(2)}`;
}

function enviarFactura() {

    Swal.fire({
        title: 'Enviando factura...',
        text: 'Por favor espera mientras procesamos los datos',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    // Obtener datos del cliente
    const cliente = {
        tipoCliente : document.getElementById('tipoCliente').value,
        tipoIdentificacion: document.getElementById('IdentificationDocumentType').value,
        identificacion: document.getElementById('identification').value,
        nombre: document.getElementById('nombre').value,
        telefono: document.getElementById('telefono').value,
        email: document.getElementById('correo').value,
        municipio: document.getElementById('municipio').value,
        direccion: document.getElementById('direccion').value,
        metodoPago: document.getElementById('metodoPago').value,
    };

    // Preparar los datos de la factura
    const factura = {
        cliente: cliente,
        productos: productosEnFactura, // Aquí va la lista de productos seleccionados
        rango : document.getElementById('rangoDocumento').value,
        aplicaIVA: document.getElementById('aplicaIVA').checked,
        retenciones: "01",
        subtotal: parseFloat(document.getElementById('subtotal').textContent.replace('$', '')),
        iva: parseFloat(document.getElementById('iva').textContent.replace('$', '')),
        total: parseFloat(document.getElementById('total').textContent.replace('$', ''))
    };

    // console.log('Factura enviada:', factura);

    // Enviar los datos al backend
    fetch('/procesar_factura/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken() // Si estás usando CSRF en Django
        },
        body: JSON.stringify(factura)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al enviar la factura');
        }
        return response.json();
    })
    .then(data => {
        console.log('Respuesta del servidor:', data);
        Swal.fire({
            icon: 'success',
            title: 'Factura enviada correctamente',
            text: 'Los datos han sido procesados exitosamente.',
        });
        
        // #rediccionar al load_facturas
        window.location.href = '/load_facturas/';
        cleanForm();
       
    })
    .catch(error => {
        console.error('Error:', error);
        Swal.fire({
            icon: 'error',
            title: 'Error al enviar la factura',
            text: 'Ocurrió un problema al procesar los datos. Por favor, intenta de nuevo.',
        });
    });
}

function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue;
}

function cleanForm(){
    productosEnFactura = [];
    actualizarTablaFactura();
    calcularTotales();
    document.getElementById('tipoCliente').value = '';
    document.getElementById('IdentificationDocumentType').value = '';
    document.getElementById('identification').value = '';
    document.getElementById('nombre').value = '';
    document.getElementById('telefono').value = '';
    document.getElementById('correo').value = '';
    document.getElementById('municipio').value = '';
    document.getElementById('direccion').value = '';
    document.getElementById('metodoPago').value = '';
    document.getElementById('rangoDocumento').value = '';
    document.getElementById('aplicaIVA').checked = false;
}


document.addEventListener('DOMContentLoaded', function () {

    load_data()
    const btnAgregarProducto = document.getElementById('agregarProducto');
    const aplicaIVA = document.getElementById('aplicaIVA');
    
    if (btnAgregarProducto) {
        btnAgregarProducto.addEventListener('click', agregarProductoAFactura);
    }
    
    if (aplicaIVA) {
        aplicaIVA.addEventListener('change', calcularTotales);
    }
    
});