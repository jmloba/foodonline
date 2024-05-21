// $('.delete_cart').on('click',function(e){
//   e.preventDefault();

//   cart_id  = $(this).attr('data-id');
//   url = $(this).attr('data-url');

//   console.log ('** delete icon -->> delete cart')
//   console.log('cart-id', cart_id )
//   console.log('data-url :', url)

//   $.ajax({
//     type: 'GET',
//     url : url,
//     success: function(response){
//       console.log(response)
           
//       if(response.status =='Failed'){
//         swal(response.message)
//       }
//       else{
   

//         $('#cart-counter').html(response.cart_counter['cart_count']);
//         swal(response.status,response.message,'success')
//         apply_cart_amounts(
//           response.cart_amount['subtotal'],
//           response.cart_amount['tax'],
//           response.cart_amount['grand_total'],
//           )          
//         removeCartItem(0,cart_id);
//         check_Cart_empty();
//       } ;
//     }
//   })
// })  

// // check if the cart is empty
// function check_Cart_empty(){
//   var cart_counter = document.getElementById("cart-counter").innerHTML

//   if (cart_counter == 0){
//     // show div id=empty-cart
//     document.getElementById('empty-cart').style.display='block';

//   }
// }
//   // delete the cart elment if the quanitty is 0
//   function removeCartItem(cartItemQty, cart_id){
//     if (cartItemQty <= 0 ){
//       document.getElementById("cart-item-"+cart_id).remove()
//     }

// }
// function  apply_cart_amounts(subtotal,tax,granndtotal){
//   if (window.location.pathname =='/cart/'){
//     $('#subtotal').html(subtotal);
//     $('#tax').html(tax);
//     $('#total').html(granndtotal);
//   }
// }
