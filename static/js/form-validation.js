// // // Example starter JavaScript for disabling form submissions if there are invalid fields
// // (function () {
// //   'use strict'

// //   // Fetch all the forms we want to apply custom Bootstrap validation styles to
// //   var forms = document.querySelectorAll('.needs-validation')

// //   // Loop over them and prevent submission
// //   Array.prototype.slice.call(forms)
// //     .forEach(function (form) {
// //       form.addEventListener('submit', function (event) {
// //         if (!form.checkValidity()) {
// //           event.preventDefault()
// //           event.stopPropagation()
// //         }

// //         form.classList.add('was-validated')
// //       }, false)
// //     })
// // })()

// // const form1 = document.getElementById('form1');
// // const order_no = document.getElementById('order_no');

// // form1.addEventListener('submits', (e) => {
// //   e.preventDefault();

// //   checkInputs();

// // });

// // function checkInputs() {
// //   const order_novalue = order_no.value.trim(); 
// // }

// // if(order_novalue === '' || order_novalue === null){
// //   setErrorFor(order_no, 'Order Number cannot be blank');
// // }

// // function setErrorFor(input, message){
// //   const formControl = input.parentElement;
// //   const small = formControl.querySelector('small');

// //   small.innerText = message;

// //   formControl.className = 'form-control error';
// // }


// const form1 = document.getElementById('form1');
// const order_no = document.getElementById('order_no');

// form1.addEventListener('submit', (e) => { // Changed 'submits' to 'submit'
//   e.preventDefault();

//   checkInputs();
// });

// function checkInputs() {
//   const order_novalue = order_no.value.trim(); 

//   if(order_novalue === '' || order_novalue === null){ // Moved this inside checkInputs function
//     setErrorFor(order_no, 'Order Number cannot be blank');
//   }
// }

// function setErrorFor(input, message){
//   const formControl = input.parentElement;
//   const small = formControl.querySelector('small');

//   small.innerText = message;

//   formControl.className = 'form-control error';
// }


