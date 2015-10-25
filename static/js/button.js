$(function() {
    $('button').click(function() {
        var user = 'arjun';
        var pass = 'password';
        $(".result").text("Processing...");
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
                $(".result").text("Success!");
                $(".cost").text("$0");
                $(".subcost").text("0");
            },
            error: function(error) {
                $(".result").text("Could not make payment. :(");
                console.log(error);
            }
        });
    });
});
