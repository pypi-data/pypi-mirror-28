/**
 * Created by richard on 11.07.17.
 */


(function(){
    $('#btn_test_mail').click(function() {
        $.ajax({
            url: '/settings/security',
            success: function (result, status, request) {
                alert(result.success);
            },
            error: function(result, status, error_code){
                console.log(JSON.stringify(result));
                alert(result.responseText);
            }
        });
    });
})();