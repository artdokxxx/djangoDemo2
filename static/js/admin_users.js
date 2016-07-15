requirejs.config({
    baseUrl: "/static/js/lib/",
    paths:{
        jquery: 'jquery-2.2.4.min',
        bootstrap: 'bootstrap.min',
        fuelux: 'fuelux.min',
        jasny_bootstrap: 'jasny-bootstrap.min'
    },
    shim: {
        'bootstrap': {
            deps: ['jquery']
        },
        'fuelux': {
            deps: ['bootstrap']
        },
        'jasny_bootstrap': {
            deps: ['jquery']
        }
    }
});

requirejs(['bootstrap', 'lodash', 'fuelux'], function() {
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

    $('.logout').on('click', function() {
        $.post(
            '/api/logout/',
            function (data) {
                window.location.reload();
            }
        );
    });

    var columns = [
        {
            label: 'Id',
            property: 'id',
            sortable: true
        },
        {
            label: 'Логин',
            property: 'username',
            sortable: true
        },
        {
            label: 'Статус',
            property: 'is_active',
            sortable: true
        },
        {
            label: 'Действия',
            property: 'action',
            sortable: false
        }
    ];

    var serialize = function(obj) {
        var str = [];
        for (var p in obj) {
            if (obj.hasOwnProperty(p)) {
                str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
            }
        }
        return str.join("&");
    };

    var dataSource = function (options, callback) {
        if (firstFlag && filter) {
            $('#listSearch').val(filter.search);
            //options.pageIndex = parseInt(filter.page)-1;
            options.filter.value = filter.filter;
            options.filter.text = $('#listFilter .dropdown-menu [data-value="'+filter.filter+'"] a').text();
        }

        var data = {
            ajax: "true",
            page: (firstFlag && filter.page) ? parseInt(filter.page) : ((options.pageIndex) ? options.pageIndex+1 : 1),
            pageSize: (firstFlag && filter.pageSize) ? parseInt(filter.pageSize) : ((options.pageSize) ? options.pageSize : 50),
            sortBy: (firstFlag && filter.sortBy) ? filter.sortBy : ((options.sortProperty) ? options.sortProperty : ''),
            sortDir: (firstFlag && filter.sortDir) ? filter.sortDir : ((options.sortDirection) ? options.sortDirection : ''),
            search: (firstFlag && filter.search) ? filter.search : ((options.search) ? options.search : ''),
            filter: (firstFlag && filter.filter) ? filter.filter : ((options.filter.value) ? options.filter.value : '')
        };
        
        firstFlag = false;
        $.ajax({
            method: "GET",
            data: data,
            url: "/api/users/get",
            success: function(result) {
                var firstItem, lastItem;
                firstItem = options.pageIndex * (options.pageSize || 50);
                lastItem = firstItem + (options.pageSize || 50);
                lastItem = (lastItem <= result.elementsCount) ? lastItem : result.elementsCount;
                var responseData = {
                    count: result.count,
                    items: (result.result) ? result.result : [],
                    page: options.pageIndex,
                    pages: result.pages,
                    start: firstItem+1,
                    end: lastItem
                };
                delete data.ajax;
                history.pushState({}, '', '?'+serialize(data));
                responseData.columns = columns;
                callback(responseData);
            }
        });
    };

    var customRowRenderer = function (helpers, callback) {
        var item = helpers.item;
        item.attr('id', 'row' + helpers.rowData.ID);
        callback();
    };

    var customColumnRenderer = function (helpers, callback) {
        var column = helpers.columnAttr;
        var rowData = helpers.rowData;
        var customMarkup = '';
        switch(column) {
            case 'username':
                customMarkup = '<a href="#">' + rowData.username + '</a>';
                break;
            case 'is_active':
                customMarkup = (rowData.is_active) ? '<span class="text-success">Активен</span>' : '<span class="text-warning">Деактивирован</span>';
                break;
            case 'action':
                customMarkup = '<a class="btn btn-default" style="margin-right: 10px" href="#" onclick="show_form('+rowData.id+')" role="button"><span class="fa fa-edit" aria-hidden="true"></span></a>';
                if (!rowData.i_am) {
                    if (rowData.is_active) {
                        customMarkup = customMarkup+'<a class="btn btn-danger" href="#" onclick="if (!confirm(\'Подтвердите деактивацию пользователя - '+rowData.username+'\')) {return false;} else {delete_user('+rowData.id+');}" role="button"><span class="fa fa-ban" aria-hidden="true"></span></a>';
                    } else {
                        customMarkup = customMarkup+'<a class="btn btn-success" href="#" onclick="if (!confirm(\'Подтвердите активацию пользователя - '+rowData.username+'\')) {return false;} else {activate_user('+rowData.id+');}" role="button"><span class="fa fa-power-off" aria-hidden="true"></span></a>';
                    }
                }
                break;
            default:
                customMarkup = helpers.item.text();
                break;
        }
        helpers.item.html(customMarkup);
        callback();
    };

    var firstFlag = true;
    var query = location.search.substring(1);
    var filter = query ? JSON.parse('{"' + query.replace(/&/g, '","').replace(/=/g,'":"') + '"}',
        function(key, value) { return key===""?value:decodeURIComponent(value) }) : {};

    $('#myRepeater').repeater({
        list_noItemsHTML: 'Ничего не найдено',
        dataSource: dataSource,
        list_columnRendered: customColumnRenderer,
        list_rowRendered: customRowRenderer
    });
});

var delete_user = function (user_id) {
    $.get(
        '/api/users/delete/'+user_id+'/',
        {},
        function(data) {
            if (!_.isUndefined(data['success'])) {
               $('#myRepeater').repeater('render');
            }
        }
    );
};

var activate_user = function (user_id) {
    $.get(
        '/api/users/activation/'+user_id+'/',
        {},
        function(data) {
            if (!_.isUndefined(data['success'])) {
               $('#myRepeater').repeater('render');
            }
        }
    );
};

var show_form = function (user_id) {
    $.post(
        '/admin/users/form/',
        {'id': user_id},
        function(data) {
            if (!_.isUndefined(data['success']) && data['success']) {
               $('#myRepeater').after(
                   data['html']
               );
                $('#form-template .modal').modal('show');
                $('#form-template .modal').on('hide.bs.modal', function (e) {
                    $('#form-template').html('');
                })
            }
        }
    );
};


var change_user = function () {
    $('#form-template .modal .alert.err').addClass('hide');
    $('#form-template .modal .alert.err').html('');
    $.post(
        '/admin/users/change/',
        $('#form-template form').serializeArray(),
        function(data) {
            if (!_.isUndefined(data['success']) && data['success']) {
               $('#form-template .modal').modal('hide');
                $('#myRepeater').repeater('render');
            } else {
                _.forEach(data['errors'], function(values, key) {
                    $('#form-template .modal .alert.err').prepend(
                        '<p> Поле "'+
                            data["fields_error"][key]
                        +'" - '+values[0]+'</p>'
                    );
                });
                $('#form-template .modal .alert.err.hide').removeClass('hide');
            }
        }
    );
};