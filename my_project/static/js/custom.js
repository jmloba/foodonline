
// cart quantity total
$(document).ready(function(){
  // -------------- add to cart

  $('.add_to_cart').on('click',function(e){
    e.preventDefault();
    product_item  = $(this).attr('data-id');
    url = $(this).attr('data-url');
    data ={product_item: product_item,} 
    $.ajax({
      type: 'GET',
      url : url,
      data : data,
      success: function(response){
        if (response.status=='login_required'){
          swal(response.message).then(function(){
            window.location ='/login'

          });
        }
        else    if(response.status =='Failed'){
          console.log(response);
             

        }else{
          // to change the total cart counter value ie. #car_counter is id
          $('#cart-counter').html(response.cart_counter['cart_count']);
          
          // to change the product quantity id=#qty-***
          $('#qty-' + product_item ).html(response.qty)
        }
        // to change the total cart counter value ie. #car_counter is id

      }
    })

  })



  // -------------- decrease cart

  $('.decrease_cart').on('click',function(e){
    e.preventDefault();
    product_item  = $(this).attr('data-id');
    url = $(this).attr('data-url');
 
    $.ajax({
      type: 'GET',
      url : url,
      success: function(response){
        // to change the total cart counter value ie. #car_counter is id
        if (response.status=='login_required'){
          swal(response.message).then(function(){
            window.location ='/login'

          });
        }
        else          
        if(response.status =='Failed'){
          console.log(response);
        }else{
           console.log('product item '+product_item)          
          $('#cart-counter').html(response.cart_counter['cart_count']);
          
          // to change the product quantity id=#qty-***
          $('#qty-' + product_item ).html(response.qty)
        }
   
        ;
      }
    })
  })



  $('.item_qty').each(function(){
      var the_id = $(this).attr('id')
      var qty = $(this).attr('data-qty')
      console.log(qty)  // show in console
      console.log(the_id)

      $('#'+the_id).html(qty);
      

  }  )

});





// // jquery
// $(document).ready(function(){
//   $('.decrease_cart').on('click',function(e){
//     e.preventDefault();
//     product_item =$(this).attr('data-id');
//     alert(product_item);    
    
//   })

// });

