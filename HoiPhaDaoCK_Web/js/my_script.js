

$(document).ready(function () {
    // $.getJSON('https://topchonlua.com/batch/data/stock_T0.json', function (response) {
    //     console.log(response);
    // });
    $.ajax({
        url: 'https://topchonlua.com/batch/data/stock_T0.json',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        type: "GET",
        dataType: "json",
        data: {
        },
        success: function (result) {
            console.log(result);
        },
        error: function () {
            console.log("error");
        }
    })
});