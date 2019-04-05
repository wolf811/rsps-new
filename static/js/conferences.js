"use_strict";
$(document).ready(function () {
    //add conference modal ajax
    $('#submit_conference_button').click((event) => {
        event.preventDefault();
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
        var conference_id = $(event.target).closest('a.btn-action').data('conference-id');
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
        // console.log('FORM_NUMBER', form_number);
        element.closest('.question_theme').hide();
        //find django hidden input and make it checked
        //django formsets works with hidden input data
        let del_input = $(`#delete_input_${conference_id}_${form_number}`).find(`#id_form-${form_number}-DELETE`)
        // let del_input = $(element).closest(`#id_form-${form_number}-DELETE`);
        // id_form-0-DELETE
        $(del_input).prop("checked", true);
        // console.log('SET CHECKED', del_input);
        let subject_list = $(`#${lst_id}`).find('.input-group-text:visible');
        //update numbers of questions in <strong> tag
        let counter = 0;
        for (el of subject_list) {
                counter++;
                let question_number = $(el).find('.question_number');
                question_number.text(counter);
        }
        let conf_data = $('td').find(`#conference_${conference_id}_form_data`);
        $(`#conference_${conference_id}_subjects`).find('.text-danger').remove();
    });

    $('.select_existing_member').click((event) => {
        if ($(".select_existing_member > input[type='radio']").is(':checked')) {
            $('#new_participant_conference_register_new').hide();
            $('#new_participant_conference_select_existing').show();
        }
    });

    $('.register_new_participant').click((event) => {
        if ($(".register_new_participant > input[type='radio']").is(':checked')) {
            $('#new_participant_conference_select_existing').hide();
            $('#new_participant_conference_register_new').show();
        }
    });

    $('td').on('click', '.register_members', (event) => {
        //clear all inputs
        let inputs = $('.modal-body').find('input');
        for (let el of inputs) {
            if ($(el).val() != '') {
                $(el).val('');
            }
        }
        //clear server_messages in form
        // update checkboxes with server data
        $('#server_messages').html('');
        var conference_id = $(event.target).closest('.btn').data('conference-id');
        var conference_title = $(`#form_${conference_id}`).find('#id_title');
        let data = {'get_checkboxes': 'true', 'conference_id': conference_id}
        $.post(`/conferences/${conference_id}/get_list_of_members/`, data)
            .done(response=>{
                console.log('CHECKBOXES', response);
                let checkboxes = $('input[name*="member"]');
                for (let el of checkboxes) {
                    //clear checked
                    $(el).prop('checked', false);
                    //set checked via response
                    if (response['checkboxes'].includes($(el).attr('id'))) {
                        $(el).prop('checked', true);
                    }
                }
            })
        $('#modal_conference_name').text($(conference_title).val());
        $('#modal_conference_name').attr("data-conference-id", conference_id);
        $('#participantConfModal').modal('show');
    });

    //handle member delete button press
    $('td').on('click', '.delete_registration', function(event) {
        event.preventDefault();
        let member_id = $(event.target)
                            .closest('a.delete_registration')
                            .data('member-id');
        let conference_id = $(event.target)
                                .closest('td.total-column')
                                .attr('id')
                                .split('_')[1];
        deleteMemberRegistration(conference_id, member_id);
    });

    $('.save_member_registrations').click((event)=>{
        event.preventDefault();
        let data= []
        if ($(".register_new_participant > input[type='radio']").is(':checked')) {
            for (element of $('#new_participant_conference_register_new').serializeArray()) {
                data.push(element);
            }
            data.push({name: 'register_new_member_adding_to_conference', value: 'True'});
        }
        if ($(".select_existing_member > input[type='radio']").is(':checked')) {
            for (element of $('#new_participant_conference_select_existing').serializeArray()) {
                data.push(element);
            }
            data.push({name: 'register_existitng_members', value: 'True'});
        }
        let conference_id = $('#modal_conference_name').data('conference-id');
        updateMembers(conference_id, data);
    });

    //update conference members
    function updateMembers(conference_id, data) {
        $.post(`/conferences/${conference_id}/update_members/`, data)
            .done(function(response) {
                $('#new_participant_conference_register_new').find('small').remove();
                if ('member_save_errors' in response) {
                    for (let err of Object.keys(response['errors'])) {
                        let form = $('#new_participant_conference_register_new');
                        let element = form.find(`input[name=${err}]`);
                        element.after(`<small class="text-danger">${response['errors'][err]}</small>`);
                    }
                } else {
                    $('.modal-body > #server_messages').html('<p class="text-success">Успешно сохранено</p>');
                    getListOfRegistrations(conference_id);
                }
            })
            .fail(function(response) {
                console.log('server not ok', response);
            });
    };

    function getListOfRegistrations(conference_id) {
        let list_of_registrations;
        $.post(`/conferences/${conference_id}/get_list_of_members/`)
            .done(response => {
                console.log('***SERVER LIST OK***');
                list_of_registrations = response;
                let tBody = $(`#conference_${conference_id}_registrations`);
                $(tBody).html(list_of_registrations);
            })
            .fail(response =>{
                console.log('***SERVER LIST ERROR***', response);
            });
        return list_of_registrations
    };

    function deleteMemberRegistration(conference_id, member_id) {
        let data = {'unregister_member': member_id};
        $.post(`/conferences/${conference_id}/unregister_members/`, data)
            .done(response => {
                if (response['status'] == 'ok') {
                    let iAmSure = confirm('Отменить регистрацию?');
                    if (iAmSure) {
                        $(`#registration_${member_id}_on_conference_${conference_id}`).remove();
                    }
                }
            })
            .fail(response => {
                console.log('***SERVER_ERR***');
                console.log(response);
            })
    };

    // $('.delete').on('click', event => {
    //     const clickedElement = $(event.target);
    //     const targetElement = clickedElement.closest('.delete');

    //     this.delete(targetElement.data('id'));
    //   });

    $('#select_all_members').click(()=>{
        let checkBoxes = $('input[name*="member"]');
        checkBoxes.prop("checked", !checkBoxes.prop("checked"));
    });

    $('td').on('click', '.save_conference_button' , (event) => {
        event.preventDefault();
        var conference = $(event.target).closest('td').attr('id');
        var conference_id = conference.match( /\d+/g)[0];
        save_conference(conference_id);
    });

    function convert_date(date) {
        let date_arr = date.split('-');
        let year = date_arr[0];
        let month = date_arr[1];
        let day = date_arr[2];
        return `${day}.${month}.${year}`;
    };

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
                    //convert date from format 'y-m-d' to 'd-m-y'
                    let date_input = $(`#td_${conference_id}`).find('.datepicker-here');
                    let date_current = $(date_input).val();
                    // console.log(date_current);
                    $(date_input).val(convert_date(date_current));
                    // console.log($(date_input));
                    // console.log(date_input);
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
                    $(`#conference_${conference_id}_subjects`).find('.text-danger').remove();
                    // handle massages
                    console.log(response);
                    // handle error server messages
                    if ('formset_errors' in response) {
                        let subjects = $(`#conference_${conference_id}_subjects`).find('.question_theme');
                        for (err of response['formset_errors']) {
                            if (err['subject']) {
                                html_err = `<small class="text-danger minus-margin-top d-block">${err['subject']}</small>`
                                $(subjects[response['formset_errors'].indexOf(err)]).after(html_err);
                            }
                            console.log(err);
                        }
                        $(`#messages_${conference_id}`).html(`<span class="text-danger">${response['message']}</span>`);
                    } else {
                        $(`#messages_${conference_id}`).html(response.message);
                    }
                    //initialize datepicker to loaded content
                    // $('.datepicker-here').datepicker();
                })
                .fail(function (response) {
                    console.log('***SERVER ERROR***');
                    console.log(response);
                });
    };

});