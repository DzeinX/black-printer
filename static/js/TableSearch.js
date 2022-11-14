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
        $('input[name="naming_wd"]').prop('checked', false)
        $('#search').val('')
        $('#search_work_done').val('')
        $('#sch1').val('')
        $('#sch2').val('')
        $('#sch3').val('')
        $('#sch4').val('')
        $('#sch5').val('')
        $("#mytable tbody tr").show()
        $(".dtls").show()
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

    $('#search_work_done').keyup(function() {
        _this = this;
        console.log(1)
        $.each($('.dtls'), function () {
            console.log(2)
            if ($(this).text().toLowerCase().indexOf($(_this).val().toLowerCase()) === -1)
                $(this).hide();
            else
                $(this).show();
        });
    });

    $('input[name="naming_wd"]').click(function () {
        _this = this;
        $.each($('.dtls'), function () {
            console.log(2)
            if ($(this).text().toLowerCase().indexOf($(_this).val().toLowerCase()) === -1)
                $(this).hide();
            else
                $(this).show();
        });
    })
});

