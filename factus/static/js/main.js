// document.addEventListener('DOMContentLoaded', function () {

//   document.querySelector('#products').addEventListener('click', () => load_products());

    
// });

// load_products()
// function load_products() {
//   fetch('/products/')
//     .then(response => {
//       if (!response.ok) {
//         throw new Error(`HTTP error! Status: ${response.status}`);
//       }
//       return response.json();
//     })
//     .then(products => {
//       products.forEach(product => {
//         console.log(product.image)

//           const col = document.createElement('div');
//           col.className = ('col g-4')
//           document.querySelector('#products').append(col)

//       });
//     })
//     .catch(error => {
//       console.error('Error fetching products:', error);
//     });
// }