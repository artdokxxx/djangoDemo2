requirejs(['main'], function (main) {
    
    require(['bootstrap', 'lodash', 'fuelux'], function () {
        var columns = [
            {
                label: 'Id',
                property: 'id',
                sortable: true
            },
            {
                label: 'Название',
                property: 'name',
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

        var serialize = function (obj) {
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
                options.filter.text = $('#listFilter .dropdown-menu [data-value="' + filter.filter + '"] a').text();
            }

            var data = {
                ajax: "true",
                page: (firstFlag && filter.page) ? parseInt(filter.page) : ((options.pageIndex) ? options.pageIndex + 1 : 1),
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
                url: "/api/categories/get",
                success: function (result) {
                    var firstItem, lastItem;
                    firstItem = options.pageIndex * (options.pageSize || 50);
                    lastItem = firstItem + (options.pageSize || 50);
                    lastItem = (lastItem <= result.elementsCount) ? lastItem : result.elementsCount;
                    var responseData = {
                        count: result.count,
                        items: (result.result) ? result.result : [],
                        page: options.pageIndex,
                        pages: result.pages,
                        start: firstItem + 1,
                        end: lastItem
                    };
                    delete data.ajax;
                    history.pushState({}, '', '?' + serialize(data));
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
            switch (column) {
                case 'name':
                    customMarkup = '<a href="#">' + rowData.name + '</a>';
                    break;
                case 'is_active':
                    customMarkup = (rowData.is_active) ? '<span class="text-success">Активна</span>' : '<span class="text-warning">Деактивирована</span>';
                    break;
                case 'action':
                    customMarkup = '<a class="btn btn-default" style="margin-right: 10px" href="#" onclick="show_form(' + rowData.id + ')" role="button"><span class="fa fa-edit" aria-hidden="true"></span></a>';
                    if (!rowData.i_am) {
                        if (rowData.is_active) {
                            customMarkup = customMarkup + '<a class="btn btn-danger" href="#" onclick="if (!confirm(\'Подтвердите деактивацию - ' + rowData.name + '\')) {return false;} else {delete_obj(' + rowData.id + ');}" role="button"><span class="fa fa-ban" aria-hidden="true"></span></a>';
                        } else {
                            customMarkup = customMarkup + '<a class="btn btn-success" href="#" onclick="if (!confirm(\'Подтвердите активацию - ' + rowData.name + '\')) {return false;} else {activate_obj(' + rowData.id + ');}" role="button"><span class="fa fa-power-off" aria-hidden="true"></span></a>';
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
        var filter = query ? JSON.parse('{"' + query.replace(/&/g, '","').replace(/=/g, '":"') + '"}',
            function (key, value) {
                return key === "" ? value : decodeURIComponent(value)
            }) : {};

        $('#myRepeater').repeater({
            list_noItemsHTML: 'Ничего не найдено',
            dataSource: dataSource,
            list_columnRendered: customColumnRenderer,
            list_rowRendered: customRowRenderer
        });
    });
});

var delete_obj = function (id) {
    $.get(
        '/api/categories/delete/'+id+'/',
        {},
        function(data) {
            if (!_.isUndefined(data['success'])) {
               $('#myRepeater').repeater('render');
            }
        }
    );
};

var activate_obj = function (id) {
    $.get(
        '/api/categories/activation/'+id+'/',
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
        '/api/categories/form/',
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


var change_obj = function () {
    $('#form-template .modal .alert.err').addClass('hide');
    $('#form-template .modal .alert.err').html('');
    $.post(
        '/api/categories/change/',
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