'use strict';
$(document).ready(function(){
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
    //django csrf tokens from cookie
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    // console.log('CSRF_TOKEN:', csrftoken);

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    // $ajaxSetup https://docs.djangoproject.com/en/2.2/ref/csrf/#ajax
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('#post-form').on('click', function(event){
        event.preventDefault();
        add_member();
    });

    $('.pencil').on('click' , function(event) {
        event.preventDefault();
        edit_member($(this).attr('href'));
    });

    $('.update_member_button').click( (event) => {
        event.preventDefault();
        console.log('update_member_button clicked');
    });

    $('.delete_member').on('click', function(event){
        event.preventDefault();
        let member_id = $(this).data('member-pk');
        let member_fio = $(this).data('member-fio');
        toggle_delete_modal(member_id, member_fio);
    });

    //bootstrap bolloons setup
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
      });

    /***dynamicly loaded form handlers***/
    //save member button handler
    $(".member_row_parent").on("click", ".update_member_button", function() {
        console.log('update_member_button clicked');
        update_member($(this).data('member-id'));
    });
    //event register
    $(".member_row_parent").on("click", ".event_register", function() {
        console.log('.event_register clicked');
        console.log($(this).data('event-id'));
        let event_id = $(this).data('event-id');
        //add event id to server request via hidden input
        $(this).parent().find('input:hidden').remove();
        if ($(this).is(':checked')) {
            $(this).after(
                `<input type='hidden' name="registered_event", value="${event_id}"></input>`
            );
        } else {
            $(this).after(
                `<input type='hidden' name="unregister_event", value="${event_id}"></input>`
            );
        }
    });

    /***member CRUD functions***/
    function add_member() {
        // console.log("create member is working!") // sanity check
        $.ajax({
            url : "", // the endpoint - current page
            type : "POST", // http method
            data : $('#add_new_member_form').serializeArray(), // data sent with the post request

            // handle a successful response
            //https://realpython.com/django-and-ajax-form-submissions/
            //http://jsn-techtips.blogspot.com/2014/04/django-show-form-validation-error-with.html

            success : function(json_result) {
                // $('#add_new_member_form').val(''); // remove the value from the input
                console.log(json_result); // log the returned json to the console
                // console.log("json response recieved"); // another sanity check
                if ('not_unique' in json_result) {
                    $('#results').html(`
                    <p class="text-info">
                    Такой пользователь уже зарегистрирован: <br>
                    <strong>${json_result['member_fio']}, идентификатор: ${json_result['member_id']}</strong>
                    </p>`);
                }
                if ('new_member_saved' in json_result) {
                    console.log('saved new member:', json_result['new_member_saved']);
                    $('#results').html(`
                    <p class="text-success">
                    Данные успешно сохранены, форму можно закрыть
                    </p>`);
                    $('#dismiss-link').text('Закрыть форму');
                    $('#dismiss-link').click(()=>{location.reload()});
                }
                //clear previous messages (if exist);
                let error_message = $('.text-danger');
                error_message.remove()
                //update fields with error messages (add after)
                for (let key in json_result) {
                    if (key in {'fio':1, 'job':1, 'jobplace':1, 'tel':1, 'email':1, 'city':1}) {
                        let error = json_result[key];
                        // console.log('error text', error);
                        let field = $('#add_new_member_form').find(`#id_${key}`);
                        for (let err of error) {
                            field.after(`
                            <small class="text-danger d-block">
                            ${err}
                            </small>`);
                        }
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
    }; //end function add member

    //progress animation on change of loading row
    $(function() {
        $(".loading_row").on("change", function() {
        //   var clientid=$("#client").val();
          $('#loadingmessage').show();
        })
    });

    function edit_member(collapse_id) {
        $(collapse_id).collapse('toggle');
        //get member_id from edit href
        let member_id = collapse_id.match(/\d+/).join("");
        // console.log(member_id);
        //now load from controller current member data
        $.ajax({
            url : '/members/edit/', // the endpoint - current page
            type : "POST", // http method
            data : {
                'member_pk': member_id,
            }, // data sent with the post request
            // handle a successful response
            // https://realpython.com/django-and-ajax-form-submissions/
            // http://jsn-techtips.blogspot.com/2014/04/django-show-form-validation-error-with.html

            success : function(response) {
                // $('#add_new_member_form').val(''); // remove the value from the input
                $('#loadingmessage').hide();
                $(`#td_${member_id}`).html(response);
                // console.log("json response recieved"); // another sanity check
                // update fields with error messages (add after)
            },

            // handle a non-successful response
            error : function(xhr) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }; //end function edit member

    function update_member(member_id) {
        // serialize form data to sent with the post request
        let serialized_data = $(`#edit_member_form_${member_id}`).serializeArray();
        //add_member primary key to request
        serialized_data.push({name:'member_pk', value:member_id});
        //add_type of request to handle by view
        serialized_data.push({name:'update_form_data', value:'True'});
        // console.log('SERIALIZED', serialized_data);
        $.ajax({
            url : '/members/edit/', // the endpoint - member edit page
            type : "POST", // http method
            // data sent with the post request
            data : serialized_data,
            // handle a successful response
            success : function(response) {
                console.log(typeof response, response); // log the returned json to the console
                //clear previous messages (if exist);
                let error_message = $(`#edit_member_form_${member_id}`).find('.text-danger');
                error_message.remove()
                //update fields with error messages (add message after field)
                for (let key in response) {
                    if (key in {'fio':1,
                                'job':1,
                                'jobplace':1,
                                'tel':1,
                                'email':1,
                                'city':1,
                                'short_description': 1}) {
                        let error = response[key];
                        // console.log('error text', error);
                        let field = $(`#edit_member_form_${member_id}`).find(`#id_${key}`);
                        for (let err of error) {
                            field.after(`
                            <small class="text-danger d-block">
                            ${err}
                            </small>`);
                        }
                    }
                }
                let server_message = $(`#edit_member_form_${member_id}`).find(`#responseMessage${member_id}`);
                server_message.html(response['message']);
                server_message.show();
                // $('#loadingmessage').hide();
            },
            // handle a non-successful response
            error : function(xhr) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }; //end function update member

    function toggle_delete_modal(member_id, member_fio) {
        $('#validation_field').val('');
        $('#wrong_input').hide();
        $('#can_be_deleted_message').hide();
        $('#confirm_deleting_form').modal('toggle');
        $('#confirm_deleting_fio').text(member_fio);
        $('#validation_field').keyup(function(){
            let input_value = $('#validation_field').val();
            if (input_value != 'УДАЛИТЬ') {
                $('#can_be_deleted_message').hide();
                $('#wrong_input').show();

            } else {
                $('#wrong_input').hide();
                $('#can_be_deleted_message').show();
            }
         });

        $('#save_delete_member_button').on('click', function(){
            event.preventDefault();
            if ($('#can_be_deleted_message').is(':visible')) {
                console.log('wi can now delet it');
                console.log('member id to delete', member_id);
                $.ajax({
                    url : '/members/delete/', // the endpoint - member edit page
                    type : "POST", // http method
                    // data sent with the post request
                    data : {'member_id': member_id},
                    // handle a successful response
                    success : function(response) {
                        console.log(typeof response, response); // log the returned json to the console
                        if (!response['error']) {
                            $('#can_be_deleted_message').html(
                                `
                                <span class="text-info">
                                <i class="fa fa-check"></i>
                                ${response.message}: "${response.fio}"
                                </span>
                                `
                            );
                        } else {
                            $('#can_be_deleted_message').hide();
                            $('#wrong_input').show();
                            $('#wrong_input').html(
                                `
                                <span class="text-danger">
                                <i class="fa fa-times"></i>
                                ${response.message}: "${response.error}"
                                </span>
                                `
                            );
                        }
                    },
                    // handle a non-successful response
                    error : function(xhr) {
                        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                    }
                });
            } else {
                console.log('confirmation not exist');
            };
        });
    };
}); //document ready end function
