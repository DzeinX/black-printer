function function_coll() {
    if ($(this).text().toLowerCase().indexOf($(_this).val().toLowerCase()) === -1)
        $($(this).parent(this)).hide();
    else
        $($(this).parent(this)).show();
}

$(document).ready(function () {
    $("#search").keyup(function () {
        _this = this;
        $.each($("#mytable tbody tr"), function () {
            if ($(this).text().toLowerCase().indexOf($(_this).val().toLowerCase()) === -1)
                $(this).hide();
            else
                $(this).show();
        });
    });

    $('input[name="status"]').click(function () {
        _this = this;
        $.each($("#mytable tbody tr td[class='4']"), function_coll);
    })

    $('input[name="naming"]').click(function () {
        _this = this;
        $.each($("#mytable tbody tr td[class='2']"), function_coll);
    })

    $('#btn_off').click(function () {
        $('input[name="status"]').prop('checked', false)
        $('input[name="naming"]').prop('checked', false)
        console.log($('#search').val(''))
        console.log($('#sch1').val(''))
        console.log($('#sch2').val(''))
        console.log($('#sch3').val(''))
        console.log($('#sch4').val(''))
        console.log($('#sch5').val(''))
        $("#mytable tbody tr").show()
    });

    $("#sch1").keyup(function () {
        _this = this;
        $.each($("#mytable tbody tr td[class='1']"), function_coll);
    });

    $("#sch2").keyup(function () {
        _this = this;
        $.each($("#mytable tbody tr td[class='2']"), function_coll);
    });

    $("#sch3").keyup(function () {
        _this = this;
        $.each($("#mytable tbody tr td[class='3']"), function_coll);
    });

    $("#sch4").keyup(function () {
        _this = this;
        $.each($("#mytable tbody tr td[class='4']"), function_coll);
    });

    $("#sch5").keyup(function () {
        _this = this;
        $.each($("#mytable tbody tr td[class='5']"), function_coll);
    });

    $("#sch6").keyup(function () {
        _this = this;
        $.each($("#mytable tbody tr td[class='6']"), function_coll);
    });

});

