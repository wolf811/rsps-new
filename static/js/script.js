'use strict';

$(function () {
  $('[data-toggle="popover"]').popover()
})

$('#showRecovery').click(function() {
	$('#pass-recovery').show('fade');
	$('#login-account').hide();
});

$('#backLogin').click(function() {
	$('#login-account').show('fade');
	$('#pass-recovery').hide();
})

// ======= Страница Регистрации - выбор типа регистрации =======
$("#regRo").change(function() {
    if ($(this).prop('checked')) {
        $('#complexUser').show('fade');
        $('#simleUser').hide();
    }
});
$("#regUser").change(function() {
    if ($(this).prop('checked')) {
        $('#simleUser').show('fade');
        $('#complexUser').hide();
    }
});
$("#imMember").change(function() {
    if ($(this).prop('checked')) {
        $('#chooseRo').show('fade');
    } else {
        $('#chooseRo').hide(); 
    }
});
// ====== END ==========

// ======= Просмотр, редактирование члена РСПС в ЛК =========
$('#addDis').click(function() {
    $('#form1').prop('disabled', 'disabled');
});
$('#removeDis').click(function() {
    $('#form1').prop('disabled', '');
});
// ====== END ==========

// ======= Статусы членов РСПС c прогресс-баром =========
$(function() {
    // Относится к статусу "Новый", где внутри профиля есть только чекбокс "ЗАЯВЛЕН"
    $("#status0").change(function() {
        if ($(this).prop('checked')) {
            $("#progressStatusNull").removeClass('bg-default text-secondary').addClass('progress-bar-striped bg-info');
        } else {
            $("#progressStatusNull").removeClass('progress-bar-striped bg-info').addClass('bg-default text-secondary');
        }
    });

    // статус "Заявлен"
    $('#status1').click(function() {
        $("#progressStatusTwo").removeClass('progress-bar-striped bg-success').addClass('bg-default text-secondary');
        $("#progressStatusThree").removeClass('progress-bar-striped bg-warning').addClass('bg-default text-secondary');
        $("#progressStatusOne").removeClass('bg-default text-secondary').addClass('progress-bar-striped bg-info');
    });
    // статус "Одобрено РСПС"
    $('#status2').click(function() {
        $("#progressStatusThree").removeClass('progress-bar-striped bg-warning').addClass('bg-default text-secondary');
        $("#progressStatusOne").removeClass('bg-default text-secondary').addClass('progress-bar-striped bg-info');
        $("#progressStatusTwo").removeClass('bg-default text-secondary').addClass('progress-bar-striped bg-success');
    });
    // статус "Сертификат РСПС"
    $('#status3').click(function() {
        $("#progressStatusOne").removeClass('bg-default text-secondary').addClass('progress-bar-striped bg-info');
        $("#progressStatusTwo").removeClass('bg-default text-secondary').addClass('progress-bar-striped bg-success');
        $("#progressStatusThree").removeClass('bg-default text-secondary').addClass('progress-bar-striped bg-warning');
    });
})
// ====== END ==========

// new member form submit
// AJAX for posting

$('#post-form').on('click', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    add_member();
});

function add_member() {
    console.log("create member is working!") // sanity check
    $.ajax({
        url : "", // the endpoint
        type : "POST", // http method
        data : $('#add_new_member_form').serializeArray(), // data sent with the post request

        // handle a successful response
        //https://realpython.com/django-and-ajax-form-submissions/
        //http://jsn-techtips.blogspot.com/2014/04/django-show-form-validation-error-with.html

        success : function(json_result) {
            // $('#add_new_member_form').val(''); // remove the value from the input
            console.log(json_result); // log the returned json to the console
            console.log("success"); // another sanity check
            for (let key in json_result) {
                if (key in {'fio':1, 'job':1, 'jobplace':1, 'tel':1, 'email':1, 'city':1}) {
                    console.log('error is here!');
                    let error = json_result[key];
                    console.log('error text', error);
                    let field = $('#add_new_member_form').find(`#id_${key}`);
                    field.before(`<p class="text-danger">${error}</p>`);
                }
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};