// Productos de ejemplo
const productosIniciales = [
    {
        codigo: 'P001',
        nombre: 'Laptop HP 15.6"',
        descripcion: 'Laptop HP con procesador Intel i5, 8GB RAM, 256GB SSD',
        precio: 799.99,
        stock: 10
    },
    {
        codigo: 'P002',
        nombre: 'Monitor Dell 24"',
        descripcion: 'Monitor LED Full HD 1080p, 60Hz',
        precio: 199.99,
        stock: 15
    },
    {
        codigo: 'P003',
        nombre: 'Teclado Mecánico RGB',
        descripcion: 'Teclado gaming con switches Blue, retroiluminación RGB',
        precio: 89.99,
        stock: 20
    },
    {
        codigo: 'P004',
        nombre: 'Mouse Inalámbrico',
        descripcion: 'Mouse ergonómico con 6 botones, 2400 DPI',
        precio: 29.99,
        stock: 30
    },
    {
        codigo: 'P005',
        nombre: 'Disco Duro Externo 1TB',
        descripcion: 'Disco duro portátil USB 3.0',
        precio: 59.99,
        stock: 25
    }
];

// Guardar productos en localStorage si no existen
if (!localStorage.getItem('productos')) {
    localStorage.setItem('productos', JSON.stringify(productosIniciales));
}

// Función para cargar productos en la tabla
function cargarProductosEnTabla() {
    const productos = JSON.parse(localStorage.getItem('productos')) || [];
    const tabla = document.getElementById('productosTabla');
    if (tabla) {
        tabla.innerHTML = productos.map(producto => `
            <tr>
                <td>${producto.codigo}</td>
                <td>${producto.nombre}</td>
                <td>$${producto.precio.toFixed(2)}</td>
                <td>${producto.stock}</td>
                <td>
                    <button class="btn btn-sm btn-warning">Editar</button>
                    <button class="btn btn-sm btn-danger">Eliminar</button>
                </td>
            </tr>
        `).join('');
    }
}

// Función para cargar productos en el select de facturación
function cargarProductosEnSelect() {
    const productos = JSON.parse(localStorage.getItem('productos')) || [];
    const select = document.getElementById('productoSelect');
    if (select) {
        select.innerHTML = `
            <option value="">Seleccionar producto...</option>
            ${productos.map(producto => `
                <option value="${producto.codigo}">${producto.nombre} - $${producto.precio.toFixed(2)}</option>
            `).join('')}
        `;
    }
}

// Cargar productos cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    cargarProductosEnTabla();
    cargarProductosEnSelect();
});