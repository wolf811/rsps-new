'use strict';

$('#showRecovery').click(function() {
	$('#pass-recovery').show('fade');
	$('#login-account').hide();
});

$('#backLogin').click(function() {
	$('#login-account').show('fade');
	$('#pass-recovery').hide();
})

// $('#selectAll').change() {
// 	if(this).prop('checked') {
// 		$("input[name='congressMan']").attr('checked', 'checked');
// 	} else {
// 		$("input[name='congressMan']").attr('checked', false);
// 	}
// }

$(document).ready(function() { 
    $(".select-all").on("change", function() {
        var groupId = $(this).data('id');
        $('.select-one[data-id="' + groupId + '"]').prop("checked", this.checked);
    });

    $(".select-one").on("change", function() {
        var groupId = $(this).data('id');
        var allChecked = $('.select-one[data-id="' + groupId + '"]:not(:checked)').length == 0;
        $('.select-all[data-id="' + groupId + '"]').prop("checked", allChecked);
    });
});


