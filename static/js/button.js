$(function() {
    $('button').click(function() {
        var user = 'arjun';
        var pass = 'password';
        $.ajax({
            url: '/api/make-payment/',
            data: JSON.stringify({"username": "arjun",
            					"password": "password",
            					"amount": "1"}),
            type: 'POST',
            contentType: "application/json",
            dataType: 'json',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});