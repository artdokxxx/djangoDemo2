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
            sortable: false
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
                customMarkup = '<a class="btn btn-default" style="margin-right: 10px" href="#" role="button"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';
                // FIXME: Add activate button if is_active false
                customMarkup = customMarkup+'<a class="btn btn-default" href="#" onclick="if (!confirm(\'Подтвердите деактивацию пользователя - '+rowData.username+'\')) {return false;} else {delete_user('+rowData.id+');}" role="button"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span></a>';
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