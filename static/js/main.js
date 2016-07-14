requirejs.config({
    baseUrl: "/static/js/lib/",
    paths: {
		jquery: 'jquery-2.2.4.min',
        bootstrap: 'bootstrap.min'
    },
    shim: {
        'bootstrap': {
            deps: ['jquery']
        }
    }
});

requirejs(['bootstrap', 'lodash'], function() {

    //https://docs.djangoproject.com/en/1.9/ref/csrf/
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

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    // Show-Hide signin form in header
    $('.user-auth .show-signin').on('click', function() {
        $(this).addClass('hide');
        $('.user-auth .reg').addClass('hide');
        $('.user-auth div.signin').removeClass('hide');
        $('.user-auth .err').addClass('hide');
    });

    $('.user-auth .btn.signin').on('click', function() {
        let showErr = function (err) {
            err = _.trim(err);
            if (_.isEmpty(err)) {
                err = "Ошибка авторизации"
            }
            $('.user-auth .err')
                .text(_.escape(err))
                .removeClass('hide');
            $('.user-auth div.signin').addClass('hide');
            $('.user-auth .show-signin').removeClass('hide');
            $('.user-auth .reg').removeClass('hide');

            return false;
        };

        let data = {
            login: _.trim($('.user-auth input[name=username]').val()),
            pwd: _.trim($('.user-auth input[name=password]').val())
        };
        
        if (_.isEmpty(data['login']) || _.isEmpty(data['pwd'])) {
            //
        } else {
            $.post(
                '/api/sign_in/',
                data,
                function (data) {
                    if (data['success'] == true) {
                        window.location.reload();
                    } else if (data['success'] == false) {
                        showErr(data['err'])
                    } else {
                        showErr();
                    }
                }
            );
        }
        return false;
    });

    $('.user-auth .btn.logout').on('click', function() {
        $.post(
            '/api/logout/',
            function (data) {
                window.location.reload();
            }
        );
    });
    
    $('.user-auth .reg').on('click', function () {
        window.location.href = '/user/registration/';
    })
});