$(document).ready(function() {
    console.log('conferences');
    $('#submit_conference_button').click((event)=>{
        event.preventDefault();
        // console.log('click');
        data = $('#add_new_conference_form').serializeArray();
        $.post('', data)
            .done(function(response){
                console.log('success');
                console.log(response);
                //handle successfully transferred data
                if ('success' in response) {
                    $('#results').html(`
                    <p class="text-success">
                    Данные успешно сохранены, форму можно закрыть
                    </p>`);
                    $('#dismiss-link').text('Закрыть форму');
                    $('#dismiss-link').click(()=>{location.reload()});
                }
                for (let key in response) {
                    if (key in {'title': 1, 'date': 1, 'place': 1}) {
                        console.log(response[key]);
                    }
                }
                //handle errors
            })
            .fail(function(response){
                console.log('fail');
                console.log(response);
            });
    })
    }
);