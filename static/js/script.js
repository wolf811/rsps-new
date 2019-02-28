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
