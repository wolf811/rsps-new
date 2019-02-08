'use strict';

$('#showRecovery').click(function() {
	$('#pass-recovery').show('fade');
	$('#login-account').hide();
});

$('#backLogin').click(function() {
	$('#login-account').show('fade');
	$('#pass-recovery').hide();
})

// Add field Conference	
// let count = 0;
// let order = document.querySelector("#orderDay");

// document.querySelector("#addQuest").onclick=function() {
// 	let quest = document.createElement("div");
// 	count++;
// 	quest.innerHTML=`
// 	<div class="form-group row align-items-center">
// 		<div class="col-sm-6 offset-sm-4">
// 			<div class="input-group input-group-sm">
// 				<div class="input-group-prepend">
// 					<span class="input-group-text" id="countQuest02"><strong>2</strong></span>
// 				</div>
// 				<input type="text" class="form-control" placeholder="Введите вопрос повестки дня">
// 				<div class="input-group-append">
// 					<button class="btn btn-outline-danger" type="button" id="button-addon2" title="Удалить вопрос"><i class="fa fa-times"></i></button>
// 				</div>
// 			</div>
// 		</div>
// 	</div>`;
// 	order.appendChild(quest);
// }

function addField() {
	alert('ghbknvkjfnv');
	// let telnum = parseInt($('#add_field_area').find('div.form-group:last').attr('id').slice(3)) 1;
	$('div#add_field_area').append(`
		<div class="form-group row align-items-center" id="add" telnum "">
			<div class="col-sm-6 offset-sm-4">
				<div class="input-group input-group-sm">
					<div class="input-group-prepend">
						<span class="input-group-text" id="countQuest02"><strong>2</strong></span>
					</div>
					<input type="text" class="form-control" placeholder="Введите вопрос повестки дня">
					<div class="input-group-append">
						<button class="btn btn-outline-danger" type="button" id="button-addon2" title="Удалить вопрос"><i class="fa fa-times"></i></button>
					</div>
				</div>
			</div>
		</div>`);
}