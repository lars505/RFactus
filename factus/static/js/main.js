document.addEventListener('DOMContentLoaded', function () {

  document.querySelector('#products').addEventListener('click', () => load_data());

    
});

load_data()
function load_data() {
    fetch('/load-data/')
    .then(response => response.json())
    .then(data => {
        cargarProductos(data.products);
        cargarTiposIdentificacion(data.document_types);
        cargarMetodosPago(data.payment_methods);
    })
    .catch(error => console.error("Error al cargar datos:", error));        
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
    const tipoIdentificacionSelect = document.getElementById('tipoCliente');
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