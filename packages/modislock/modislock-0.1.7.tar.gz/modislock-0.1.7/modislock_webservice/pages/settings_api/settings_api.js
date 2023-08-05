

(function(){
    var api_editor = new $.fn.dataTable.Editor({
        table: "#api_table",
        idSrc: 'app_id',
        ajax: {
            create: {
                type: 'POST',
                url: '/settings/api/api_tokens'
            },
            edit: {
                type: 'PUT',
                url:  '/settings/api/api_tokens'
            },
            remove: {
                type: 'DELETE',
                url:  '/settings/api/api_tokens'
            }
        },
        fields: [
            {
                label: "Application Name:", name: "app_id", type: "text",
                attr: {
                    maxlength: 25,
                    placeholder: 'Application Name'
                }
            },
            {
                label: "Secret:", name: "app_secret", type: "text",
                attr: {
                    maxlength: 25,
                    placeholder: 'My Secret'
                }
            }
        ]
    });

    var api_table = $('#api_table').DataTable({
        ordering: false,
        info: false,
        paging: false,
        searching: false,
        responsive: true,
        orderable: false,
        select: true,
        dom: "Bfrtip",
        ajax: {
            url: '/settings/api/api_tokens'
        },
        columnDefs: [
            {
                // Generic all targets
                className: 'text-center',
                targets: '_all'
            }
        ],
        columns:[
            {
                data: 'app_id'
            },
            {
                data: 'token'
            },
            {
                data: null,
                render: function(data, type, row){
                    var valid_time = moment(data.expires);

                    return ( moment(data.expires) < moment.now() ) ?
                        '<i class="text-danger">' + valid_time.format('YYYY-MM-DD HH:mm') + '</i>' :
                        '<i class="text-info">' + valid_time.format('YYYY-MM-DD HH:mm') + '</i>';
                }
            }
        ],
        buttons: [
            {
                extend: "create",
                text: "<i class='fa fa-plus text-success'></i>&nbsp Add Token",
                editor: api_editor
            },
            {
                extend: "remove",
                text: "<i class='fa fa-trash-o text-danger'></i>&nbsp Delete Token",
                editor: api_editor
            },
            {
                extend: "edit",
                text: "<i class='fa fa-file text-info'></i>&nbsp Renew Token",
                editor: api_editor
            }
        ]
    });
})();