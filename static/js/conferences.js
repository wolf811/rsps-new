"use_strict";
$(document).ready(function () {
    //add conference modal ajax
    $('#submit_conference_button').click((event) => {
        event.preventDefault();
        // console.log('click');
        let data = $('#add_new_conference_form').serializeArray();
        $.post('', data)
            .done(function (response) {
                console.log('success');
                console.log(response);
                //handle successfully transferred data
                if ('success' in response) {
                    $('#results').html(`
                    <p class="text-success">
                        Данные успешно сохранены, форму можно закрыть
                    </p>`);
                    $('#dismiss-link').text('Закрыть форму');
                    $('#dismiss-link').click(() => {
                        location.reload()
                    });
                }
                //handle errors
                for (let key in response) {
                    if (key in {'title': 1, 'date': 1, 'place': 1}) {
                        let error = response[key]
                        let field = $('#add_new_conference_form').find(`#id_${key}`);
                        for (let err of error) {
                            let err_html = `<small class="text-danger d-block">${err}</small>`;
                            if (field.attr('id') == 'id_date') {
                                picker = $('#add_new_conference_form').find('.input-group-append');
                                picker.after(err_html);
                            } else {
                                field.after(err_html);
                            }
                        }
                    }
                }
            })
            .fail(function (response) {
                console.log('***FAIL***');
                console.log(response);
            });
    });
    //edit conference ajax
    $('.conference_edit').click((event) => {
        event.preventDefault();
        var conference_id = $(event.target).parent().data('conference-id');
        edit_conference(conference_id);
        $(`#multiCollapseConf${conference_id}`).toggle();
    });
    //delegate event handler to dinamic loaded content
    $('td').on("click", ".add_question", (event) => {
        event.preventDefault();
        var conference_id = $(event.target).data('conference-id');
        var lst_input_groups = $(`#conference_${conference_id}_subjects`).find('.input-group-text');
        var html_question = `
            <div class="question_theme input-group input-group-sm mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text" id="form-${lst_input_groups.length}-id"><strong class="question_number">${lst_input_groups.length+1}</strong></span>
                </div>
                <input type="text" name="form-${lst_input_groups.length}-subject" id="id_form-${lst_input_groups.length}-subject" class="form-control" placeholder="Введите вопрос повестки дня">
                <div class="input-group-append">
                    <button data-form-number="NEW_SUBJECT" class="remove_question btn btn-outline-danger" type="button" title="Удалить вопрос"><i class="fa fa-times"></i></button>
            </div>
            </div>`;
            // <input type="text" name="form-0-subject" id="id_form-0-subject" placeholder="Введите вопрос повестки дня" class="form-control form-control-sm">
        var lst = $(`#conference_${conference_id}_subjects`);
        lst.append(html_question);
        let conf_data = $('td').find(`#conference_${conference_id}_form_data`);
        for (el of conf_data.children()) {
            if ($(el).attr('id') == 'id_form-TOTAL_FORMS') {
                // let val = $(el).attr('value');
                $(el).val(lst_input_groups.length+1+"");
            }
        }
    });

    //remove quesitons handler (updating question number)
    $('td').on("click", ".remove_question", (event) => {
        event.preventDefault();
        let element = $(event.target);
        let lst_id = element.closest('.question_list').attr('id');
        let pattern = /\d+/g;
        let conference_id = lst_id.match(pattern);
        let form_number = element.closest('button').data('form-number');
        console.log('FORM_NUMBER', form_number);
        element.closest('.question_theme').remove();
        //find django hidden input and make it checked
        //django formsets works with hidden input data
        let del_input = $(`#delete_input_${conference_id}_${form_number}`).find(`#id_form-${form_number}-DELETE`)
        $(del_input).prop("checked", true);
        // id_form-0-DELETE

        let subject_list = $(`#${lst_id}`).find('.input-group-text');
        //update numbers of questions in <strong> tag
        let counter = 0;
        for (el of subject_list) {
                counter++;
                let question_number = $(el).find('.question_number');
                question_number.text(counter);
        }
        let conf_data = $('td').find(`#conference_${conference_id}_form_data`);
        for (el of conf_data.children()) {
            if ($(el).attr('id') == 'id_form-TOTAL_FORMS') {
                // let val = $(el).attr('value');
                $(el).val(counter);
            }
        }
    });

    $('td').on('click', '.save_conference_button' , (event) => {
        event.preventDefault();
        var conference = $(event.target).closest('td').attr('id');
        var conference_id = conference.match( /\d+/g)[0];
        save_conference(conference_id);
    });

    function edit_conference(conference_id) {
        // console.log(conference_id);
        var data = {
            'conference_id': conference_id
        };
        if ($(`#form_${conference_id}`).length == 0) {
            $.post('/conferences/edit/', data)
                .done(function (response) {
                    $('#loadingmessage').hide();
                    $(`#td_${conference_id}`).html(response);
                    //initialize datepicker to loaded content
                    $('.datepicker-here').datepicker();
                })
                .fail(function (response) {
                    console.log('***ERROR***');
                    console.log(response);
                });
        }
    };

    function save_conference(conference_id) {
        console.log('SAVING', conference_id);
        let data = $('td').find(`#form_${conference_id}`).serializeArray();
        data.push({name: 'saving_conference', value: 'True'});
        data.push({name: 'conference_id', value: conference_id});
        console.log('SERIALIZED FORM', data);
        $.post('/conferences/edit/', data)
                .done(function (response) {
                    // handle massages
                    $(`#messages_${conference_id}`).html(response.message);
                    // handle error server messages
                    if ('errors' in response) {
                        for (err of response['errors']) {
                            console.log(err);
                        }
                    }
                    //initialize datepicker to loaded content
                    // $('.datepicker-here').datepicker();
                })
                .fail(function (response) {
                    console.log('***ERROR***');
                    console.log(response);
                });
    };

});