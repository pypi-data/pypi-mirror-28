$(document).ready(function() {
    $("#tz_zone").select2({
        theme: "bootstrap"
    });

    $('#rootwizard').bootstrapWizard({
        withVisible: false,
            
        onNext: function(tab, navigation, index) {
            var serialLength = 8;
            var adm_passwd_length = 8;
            // https://html.spec.whatwg.org/multipage/input.html#valid-e-mail-address for email regex per html5
            var email_rule = /^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/i
            var hide_time = 400;
            var show_time = 3000;

            // Serial Number
            if(index===1) {
                if( !$('#serial_number').val() || (($('#serial_number').val().length) !== serialLength)) {
                    $('#serial_message').html('Please enter the correct serial number').show();
                    $('#serial_number').focus();
                    setTimeout(function(){
                        $("#serial_message").hide(hide_time);
                    }, show_time);
                    return false;
                } else {
                    $('#serial_entered').html($('#serial_number').val()).show();
                }
            }

            // Serial Number Confirmation
            if(index===2) {
                // Nothing here
            }

            // Admin account Username and Email
            if(index===3) {
                if(!$('#first_name').val()) {
                    $('#first_name_message').html('Please enter the correct name').show();
                    $('#first_name').focus();
                    setTimeout(function(){
                        $("#first_name_message").hide(hide_time);
                    }, show_time);
                    return false;
                } else if(!$('#last_name').val()) {
                    $('#last_name_message').html('Please enter the correct name').show();
                    $('#last_name').focus();
                    setTimeout(function(){
                        $("#last_name_message").hide(hide_time);
                    }, show_time);
                    return false;
                } else if (!(email_rule.test($('#email').val()))) {
                    $('#email_message').html("Please enter a valid email address").show();
                    $('#email').focus();
                    setTimeout(function(){
                        $('#email_message').hide(hide_time);
                    }, show_time);
                    return false;
                } else {
                    $('#username_entered').html($('#first_name').val()+" "+$('#last_name').val()).show();
                    $('#email_entered').html($('#email').val()).show();
                }
            }

            // Admin account Username and Email Confirmation
            if(index===4) {
                // nothing here
            }

            // Admin account Password and confirmation
            if(index===5) {
                if (!$('#password').val() || (($('#password').val().length) < adm_passwd_length)) {
                    $('#password_message').html("Must be at least "+adm_passwd_length+" places long").show();
                    $('#password').focus();
                    setTimeout(function(){
                        $("#password_message").hide(hide_time);
                    }, show_time);
                    return false;
                } else if($('#pwd_confirm').val() != $('#password').val()) {
                    $('#confirm_message').html('Passwords do not match').show();
                    $('#pwd_confirm').focus();
                    setTimeout(function(){
                        $("#confirm_message").hide(hide_time);
                    }, show_time);
                    return false;
                } else {
                    $('#hours').val(moment().hour());
                    $('#minutes').val(moment().minute());
                }
            }
            // moment(data).format('YYYY-MM-DD HH:mm:ss')
                // Current Time
            if(index===6) {
                var hour = $('#hours').val();
                var minute = $('#minutes').val();

                if( (hour < 0) || (hour >= 24)) {
                    $('#cur_time_message').html('Please enter the current time').show();
                    $('#hours').focus();
                    setTimeout(function(){
                        $("#cur_time_message").hide(hide_time);
                    }, show_time);
                    return false;
                }

                if( (minute < 0) || (minute >= 60)) {
                    $('#cur_time_message').html('Please enter the current time').show();
                    $('#minutes').focus();
                    setTimeout(function(){
                        $("#cur_time_message").hide(hide_time);
                    }, show_time);
                    return false;
                }

                if(!$('#tz_zone').val()) {
                    $('#cur_tzone_message').html('Please select the current time zone').show();
                    $('#tz_zone').focus();
                    setTimeout(function(){
                        $("#cur_tzone_message").hide(hide_time);
                    }, show_time);
                    return false;
                } else {
                    $('#cur_time_entered').html("<h2>You entered: " + "<b>"+ hour + ":" + minute + "</b></h2> <h5>And</h5> <h2><b>"+$('#tz_zone').val() + "</b></h2> <h5>for timezone</h5> <h5>If correct, select <b>Next</b> to continue</h5>");
                }
            }

            // Final Confirmation
            if(index===7) {
                // $('#final_review').html("Serial Number: " + $('#serial_number').val()).show()
            }
        }
    });

    $('#rootwizard .finish').click(function() {
        $('#welcomeForm').submit();
    });
        
    // window.prettyPrint && prettyPrint()

});