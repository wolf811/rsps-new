"use_strict";
$(document).ready(function () {
    console.log('conferences');
    //add conference modal ajax
    $('#submit_conference_button').click((event) => {
        event.preventDefault();
        // console.log('click');
        data = $('#add_new_conference_form').serializeArray();
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
                for (let key in response) {
                    if (key in {
                            'title': 1,
                            'date': 1,
                            'place': 1
                        }) {
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
                //handle errors
            })
            .fail(function (response) {
                console.log('fail');
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
        var lst = $(document).find(`#conference_${conference_id}_subjects`);
        var html_question = `
            <div class="question_theme input-group input-group-sm mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text" id="countQuest01"><strong class="question_number">${lst.children().length+1}</strong></span>
                </div>
                <input type="text" class="form-control" placeholder="Введите вопрос повестки дня">
                <div class="input-group-append">
                    <button class="remove_question btn btn-outline-danger" type="button" title="Удалить вопрос"><i class="fa fa-times"></i></button>
            </div>
            </div>`;
        lst.append(html_question);
    });

    $('td').on("click", ".remove_question", (event) => {
        event.preventDefault();
        let element = $(event.target);
        let lst_id = element.closest('.col-sm-8').attr('id');
        element.closest('.question_theme').remove();
        let updated_lst = $(document).find(`#${lst_id}`).children();
        //update numbers of questions in <strong> tag
        let counter = 1;
        for (el of updated_lst) {
            let question_number = $(el).find('.question_number');
            question_number.text(counter);
            counter++;
        }
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

});