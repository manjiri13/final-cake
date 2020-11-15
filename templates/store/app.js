$(function() {
   
    var form = $('#ajax-contact');

    var formMessages = $('#form-messages');
 
});

$(form).submit(function(event) {
   
    event.preventDefault();

  
});

var formData = $(form).serialize();

$.ajax({
    type: 'POST',
    url: $(form).attr('action'),
    data: formData
})
.done(function(response) {
  
    $(formMessages).removeClass('error');
    $(formMessages).addClass('success');


    $(formMessages).text(response);

 
    $('#weight').val('');
    $('#base').val('');
    $('#sponge').val('');
    $('#flavour').val('');
    $('#cream').val('');
    $('#message').val('');
   
})
.fail(function(data) {
    
    $(formMessages).removeClass('success');
    $(formMessages).addClass('error');


    if (data.responseText !== '') {
        $(formMessages).text(data.responseText);
    } else {
        $(formMessages).text('Oops! An error occured and your data could not be sent.');
    }
});

