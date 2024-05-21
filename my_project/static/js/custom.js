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
        console.log(response)
        if (response.status=='login_required'){
          swal(response.message).then(function(){
            window.location ='/login'
          });
        }
        else if(response.status =='Failed'){
          swal(response.message)
        }else{
          // to change the total cart counter value ie. #car_counter is id
          $('#cart-counter').html(response.cart_counter['cart_count']);
      
          // to change the product quantity id=#qty-***
          $('#qty-' + product_item ).html(response.qty)
          // display subtotals and apply_cart_amounts() 
          apply_cart_amounts(
            response.cart_amount['subtotal'],
            response.cart_amount['tax_dict'],
            response.cart_amount['grand_total'],
            )
          
        }
      }
    })

  })
  // -------------- decrease cart

  $('.decrease_cart').on('click',function(e){
    e.preventDefault();
    product_item  = $(this).attr('data-id');
    url = $(this).attr('data-url');
    cart_id  = $(this).attr('id');
    $.ajax({
      type: 'GET',
      url : url,
      success: function(response){
        console.log(response)
        // to change the total cart counter value ie. #car_counter is id
        if (response.status=='login_required'){
          swal(response.message).then(function(){
            window.location ='/login'
          });
        }
        else if(response.status =='Failed'){
          swal(response.message)
        }else{
          $('#cart-counter').html(response.cart_counter['cart_count']);
          // to change the product quantity id=#qty-***
          $('#qty-' + product_item ).html(response.qty)

          apply_cart_amounts(
            response.cart_amount['subtotal'],
            response.cart_amount['tax_dict'],
            response.cart_amount['grand_total'],
            )          
          if (window.location.pathname ='/cart/') {
            removeCartItem(response.qty,cart_id)
            check_Cart_empty()
          }

          
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

  $('.delete_cart').on('click',function(e){
    e.preventDefault();
  
    cart_id  = $(this).attr('data-id');
    url = $(this).attr('data-url');
  
    console.log ('** delete icon -->> delete cart')
    console.log('cart-id', cart_id )
    console.log('data-url :', url)
  
    $.ajax({
      type: 'GET',
      url : url,
      success: function(response){
        console.log(response)
             
        if(response.status =='Failed'){
          swal(response.message)
        }
        else{
     
  
          $('#cart-counter').html(response.cart_counter['cart_count']);
          swal(response.status,response.message,'success')
          apply_cart_amounts(
            response.cart_amount['subtotal'],
            response.cart_amount['tax_dict'],
            response.cart_amount['grand_total'],
            )      
          console.log('cart amount',+response.cart_amount['tax'])      
          removeCartItem(0,cart_id);
          check_Cart_empty();

        } ;
      }
    })
  })  
  
  $('.add-hour').on('click',function(e){
    e.preventDefault();
    var day = document.getElementById('id_day').value
    var from_hour = document.getElementById('id_from_hour').value
    var to_hour = document.getElementById('id_to_hour').value
    var is_closed = document.getElementById('id_is_closed').checked
    var csrf_token = $('input[name=csrfmiddlewaretoken]').val()

    // from form = add hidden input above button
    var url = document.getElementById('add_hour_url').value

    console.log('values from page : ',day,from_hour, to_hour, is_closed,csrf_token)


    if(is_closed){
      is_closed= 'True'
      condition ="day != ''"
    } else {
      is_closed= 'False'
      condition = "day != '' && from_hour != '' && to_hour != ''"
    }

    if (eval(condition)){
      // swal('REady to add field','add the entry  to record','success')
      $.ajax( {
        type: 'POST',
        url : url,
        data : {
          'day': day, 
          'from_hour': from_hour, 
          'to_hour':to_hour, 
          'is_closed':is_closed,
          'csrfmiddlewaretoken':csrf_token,
        },
        success : function(response){
          if( response.status =='success'){
            if (response.from_hour){
              html ='<tr id="hour-'+response.id+'" ><td style="color: blue;"><b>'+response.day+'</b></td><td>'+response.from_hour+' - '+response.to_hour+'</td><td><a href="#" class="remove_item" data-url="/vendor/opening_hours/remove/'+response.id+'/">Remove</a></td></tr>'


            }
            else{
              html ='<tr id="hour-'+response.id+' ><td style="color: blue;"><b>'+response.day+'</b></td><td>Closed</td><td><a href=""  class="remove_item" data-url="/vendor/opening_hours/remove/'+response.id+'/">Remove</a></td></tr>'

            }
            // append html to table
            $('.opening_hours').append(html)
            // reset the form 
            document.getElementById('opening_hours_form').reset()
          }else{
            console.log('database message:',response.error)
            swal(response.message,'','error')

          }
    
        }

      })
    } else {
      swal('Failed','Please fill the fields required', 'info')
    }
  })

  $(document).on('click','.remove_item', function(e){
    e.preventDefault();
    url= $(this).attr('data-url');
    console.log ('passed url is : ', url)
    $.ajax({
      type:'GET',
      url:url,
      success:function(response){
          // console.log(response)
          if (response.status=='success'){
            document.getElementById("hour-"+response.id).remove()
            // swal(response.status,response.message,'success')
          }
      }
    })

  });

  $(document).on('click','.testarea-remove', function(e){
    e.preventDefault();
    url= $(this).attr('data-url');
    console.log ('passed url is : ', url)
    $.ajax({
      type:'GET',
      url:url,
      success:function(response){
          // console.log(response)
          if (response.status=='success'){
            document.getElementById("testarea-tr-"+response.id).remove()
            // swal(response.status,response.message,'success')
          }
      }
    })

  });

  function removeCartItem(cartItemQty, cart_id){
      if (cartItemQty <= 0 ){
        document.getElementById("cart-item-"+cart_id).remove()
      }
  
  }
// check if the cart is empty
  function check_Cart_empty(){
    var cart_counter = document.getElementById("cart-counter").innerHTML
  
    if (cart_counter == 0){
      // show div id=empty-cart
      document.getElementById('empty-cart').style.display='block';

    }
  }

  function  apply_cart_amounts(subtotal,tax_dict,granndtotal){
    if (window.location.pathname =='/cart/'){
      $('#subtotal').html(subtotal);
       $('#total').html(granndtotal);
      console.log('tax_dict :', tax_dict)

      for (key1 in tax_dict){
        console.log('value of ',key1, tax_dict[key1])

        for(key2 in tax_dict[key1]){
          console.log('value amount ',tax_dict[key1][key2])
          $('#tax-'+key1).html(tax_dict[key1][key2]);
          
        }
      }
    }
  }
 
  let autocomplete;
  function initAutoComplete(){
  autocomplete = new google.maps.places.Autocomplete(
      document.getElementById('id_address'),
      {
          types: ['geocode', 'establishment'],
          //default in this app is "IN" - add your country code
          componentRestrictions: {'country': ['ph']},
      }
  
      )
  // function to specify what should happen when the prediction is clicked
  autocomplete.addListener('place_changed', onPlaceChanged);
  }

  function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        // console.log('place name=>', place.name)
    }

    var geocoder = new google.maps.Geocoder()
  
    var address = document.getElementById('id_address').value

    geocoder.geocode({'address':address}, function(results,status) {
        console.log('results : ',results)
        // console.log('status :',status)

        if (status == google.maps.GeocoderStatus.OK){

          var latitude = results[0].geometry.location.lat()
          var longitude = results[0].geometry.location.lng()
          // console.log('latitude : ',latitude)
          // console.log('longitude : ',longitude)
            $('#id_latitude').val(latitude)
            $('#id_longitude').val(longitude)
            $('#id_address').val(address)
        }

      });
      // loop thru the address components
      // console.log(place.address_components);
      for( var i=0; i<place.address_components.length; i++){
        for( var j=0; j<place.address_components[i].types.length; j++){
          console.log(place.address_components[i].long_name)
          console.log(place.address_components[i].types)


          if (place.address_components[i].types[j] == 'country'){
            $('#id_country').val(place.address_components[i].long_name)
          } 
          if (place.address_components[i].types[j] == 'administrative_area_level_2') {
            $('#id_province').val(place.address_components[i].long_name)
          }else if (place.address_components[i].types[j] == 'administrative_area_level_1') {
            $('#id_province').val(place.address_components[i].long_name)
          }

          if (place.address_components[i].types[j] == 'postal_code'){
            $('#id_zip_code').val(place.address_components[i].long_name)
          } else {
            $('#id_zip_code').val('')
          }
          

        }

      }


}

});



