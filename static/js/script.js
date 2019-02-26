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

<<<<<<< HEAD
// ======= Просмотр, редактирование члена РСПС в ЛК =========
$('#addDis').click(function() {
    $('#form1').prop('disabled', 'disabled');
});
$('#removeDis').click(function() {
    $('#form1').prop('disabled', '');
});
// ====== END ==========
=======
$('#addDis').click(function() {
    $('#form1').prop('disabled', 'disabled');
});

$('#removeDis').click(function() {
    $('#form1').prop('disabled', '');
});
// $(function(){
//     $('fieldset').attr('disabled', 'disabled');

//     $('#addDis').click(function(){
//       alert($(this).attr('disabled'));
//   });
// });
>>>>>>> e584f8ee237500dca473df5b743853a4ec337698
