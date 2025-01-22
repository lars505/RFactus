// Variables globales para la factura
let productosEnFactura = [];

// Función para agregar producto a la factura
function agregarProductoAFactura() {
    const productoSelect = document.getElementById('productoSelect');
    const cantidadInput = document.getElementById('cantidad');
    const productos = JSON.parse(localStorage.getItem('productos')) || [];
    
    const producto = productos.find(p => p.codigo === productoSelect.value);
    if (!producto) return;

    const cantidad = parseInt(cantidadInput.value);
    if (cantidad <= 0 || cantidad > producto.stock) {
        alert('Cantidad no válida o insuficiente stock');
        return;
    }

    const productoEnFactura = {
        ...producto,
        cantidad,
        subtotal: producto.precio * cantidad
    };

    productosEnFactura.push(productoEnFactura);
    actualizarTablaFactura();
    calcularTotales();
    
    // Resetear campos
    productoSelect.value = '';
    cantidadInput.value = '1';
}

// Función para eliminar producto de la factura
function eliminarProductoDeFactura(codigo) {
    productosEnFactura = productosEnFactura.filter(p => p.codigo !== codigo);
    actualizarTablaFactura();
    calcularTotales();
}

// Función para actualizar la tabla de la factura
function actualizarTablaFactura() {
    const tabla = document.getElementById('productosFactura');
    if (!tabla) return;

    tabla.innerHTML = productosEnFactura.map(producto => `
        <tr>
            <td>${producto.nombre}</td>
            <td>$${producto.precio.toFixed(2)}</td>
            <td>${producto.cantidad}</td>
            <td>$${producto.subtotal.toFixed(2)}</td>
            <td>
                <button class="btn btn-sm btn-danger" onclick="eliminarProductoDeFactura('${producto.codigo}')">
                    Eliminar
                </button>
            </td>
        </tr>
    `).join('');
}

// Función para calcular totales
function calcularTotales() {
    const subtotal = productosEnFactura.reduce((sum, producto) => sum + producto.subtotal, 0);
    const aplicaIVA = document.getElementById('aplicaIVA').checked;
    const iva = aplicaIVA ? subtotal * 0.12 : 0;
    const total = subtotal + iva;

    document.getElementById('subtotal').textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById('iva').textContent = `$${iva.toFixed(2)}`;
    document.getElementById('total').textContent = `$${total.toFixed(2)}`;
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    const btnAgregarProducto = document.getElementById('agregarProducto');
    const aplicaIVA = document.getElementById('aplicaIVA');
    
    if (btnAgregarProducto) {
        btnAgregarProducto.addEventListener('click', agregarProductoAFactura);
    }
    
    if (aplicaIVA) {
        aplicaIVA.addEventListener('change', calcularTotales);
    }
});