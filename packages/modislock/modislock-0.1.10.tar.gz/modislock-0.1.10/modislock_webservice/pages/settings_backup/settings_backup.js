/**
 * Created by richard on 11.07.17.
 */

(function(){
    $('#submit_restore').click(function() {
        event.preventDefault();
        var form_data = new FormData($('#restore_db_form')[0]);

        $.ajax({
            type: 'POST',
            url: '/settings/backup/run_restore',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: false
        }).done(function(data, textStatus, jqXHR){
            toastr.success(data['success'], 'DATABASE');
        }).fail(function(data){
            toastr.error(data['error'], 'DATABASE');
        });
    });

    $(".btn-upload-4").on("click", function() {
        $("#btn_restore_db").fileinput('upload');
    });

    $(".btn-reset-4").on("click", function() {
        $("#btn_restore_db").fileinput('clear');
    });

    $("#purge_btn").confirmation({
        title: 'Confirm Purge all Events',
        btnOkClass: 'btn-xs btn-danger',
        btnOkIcon: 'fa fa-exclamation',
        btnOkLabel: 'Purge All',
        btnCancelClass: 'btn-xs btn-default',
        btnCancelIcon: 'fa fa-close',
        btnCancelLabel: 'Cancel',
        onConfirm: function() {
            $.ajax({
                url: '/settings/backup',
                type: 'POST',
                data: {action : 'purge'}
            }).done(function(data, textStatus, jqXHR){
                toastr.success(data['success'], 'DATABASE')
            }).fail(function(data){
                toastr.error(data['error'], 'DATABASE')
            })
        },
        onCancel: function() {
            console.log('Purge cancelled')
        }
    });

    // Reboot bootstrap confirmation
    $("#reboot_btn").confirmation({
        title: 'Confirm Reboot',
        btnOkClass: 'btn-xs btn-danger',
        btnOkIcon: 'fa fa-check',
        btnOkLabel: 'Reboot',
        btnCancelClass: 'btn-xs btn-default',
        btnCancelIcon: 'fa fa-close',
        btnCancelLabel: 'Cancel',
        onConfirm: function() {
            $.ajax({
                url: '/settings/backup',
                type: 'POST',
                data: {action : 'reboot'},
                success: function(){
                    window.location.href = '/settings/reboot'
                },
                error: function(response){
                    toastr.error(response.responseJSON.error, 'DATABASE')
                }
            });
        },
        onCancel: function() {
            console.log('Reboot option cancelled')
        }
    });
})();
