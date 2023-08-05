/**
 * Created by richard on 20.05.17.
 */
(function() {
    // Live refresh of data
    setInterval(update_system_info, 1000);

    $('#btn_time_set').click(function(){
        var current = moment();

        $('#hours').val(current.hours());
        $('#minutes').val(current.minutes());
    });

    $('#log_output').highlightWithinTextarea({
        highlight: [
            {
                highlight: /error/gi,
                className: 'red'
            },
            {
                highlight: /warning/gi,
                className: 'yellow'
            },
            {
                highlight: /info/gi,
                className: 'blue'
            }
        ]
    });

    $('#hours').TouchSpin({
        min: 0,
        max: 23,
        step: 1,
        decimals: 0,
        prefix: 'hrs'
    });

    $('#minutes').TouchSpin({
        min: 0,
        max: 59,
        step: 1,
        decimals: 0,
        prefix: 'mins'
    });

    $("#tz_zone").select2({
        theme: "bootstrap"
    });
})();

/**
 *   @brief Seperates values into a 50% 25% 25% ratio for colored progress bar
 *   @param input numerical value between 0 and 100
 */
function get_progress_values(input){
    var ret_values = [0, 0 ,0];

    if(input > 100){
        return ret_values;
    } else {
        ret_values[0] = input;
    }

    if(input > 50){
        ret_values[1] = ret_values[0] - 50; // Remainder stored
        ret_values[0] = 50;                 // Max is 50%
        if(ret_values[1] > 25){
            ret_values[2] = ret_values[1] - 25; // Remainder stored
            ret_values[1] = 25;
        }
    }

    return ret_values;
}

/**
 * @brief Updates live data elements
 */
function update_system_info(){
    $.ajax({
        url: "/system/status",
        success: function(result) {
            // Memory totals
            var mem = get_progress_values(result.memory_usage);
            $('#memory_info_header').html(result.memory_usage + '% of ' + (result.memory_total/1000000000).toFixed(2) + 'GB Used');
            $('#memory1').css({'width': mem[0] + '%'});
            $('#memory2').css({'width': mem[1] + '%'});
            $('#memory3').css({'width': mem[2] + '%'});

            // CPU Totals
            var cpu = get_progress_values(result.cpu_load[0]);
            $('#cpu_info_header').html(result.cpu_load[0] + '%');
            $('#cpu1').css({'width': cpu[0] + '%'});
            $('#cpu2').css({'width': cpu[1] + '%'});
            $('#cpu3').css({'width': cpu[2] + '%'});

            // Storage
            var storage = get_progress_values(result.storage);
            $('#storage_info_header').html(result.storage + '% of 4GB Used');
            $('#storage1').css({'width': storage[0] + '%'});
            $('#storage2').css({'width': storage[1] + '%'});
            $('#storage3').css({'width': storage[2] + '%'});

            // Times returned as Mon, 19 Jun 2017 19:57:17 GMT
            uptime = result.uptime.split(':');
            $('#uptime_info').html(uptime[0] + 'h ' + uptime[1] + 'm ' + uptime[2] + 's');
            $('#system_time_info').html(result.time);

            // Readers
            $.each(result.readers, function(index, value){
                if(value === 'DISCONNECTED'){
                    console.log('Disconnected');
                    $('#reader' + index + '_header').html('<div class="led-red"></div>');
                    $('#reader' + index + '_info').html(value);
                } else if(value === 'CONNECTED') {
                    console.log('Connected');
                    $('#reader' + index + '_header').html('<div class="led-green"></div>');
                    $('#reader' + index + '_info').html(value);
                }
            });

            // Sensors
            $.each(result.sensors, function(index, value){
                if(value === 'INACTIVE'){
                    $('#door' + index + '_header').html('<i class="fa fa fa-sign-in fa-2x"></i>');
                    $('#door' + index + '_info').html(value);
                } else if(value === 'ACTIVE'){
                    $('#door' + index + '_header').html('<i class="fa fa fa-sign-out fa-2x"></i>');
                    $('#door' + index + '_info').html(value);
                }
            });
        },
        error: function(msg) {
            console.log('Error in request');
        }
    });
}

/*
 * @brief Fetches latest software releases for Webadmin and Host Monitor for the update modal window
 */
function get_versions( current_modislock_ver, avail_modislock_ver, current_monitor_ver, avail_monitor_ver){
    current_modislock_ver = current_modislock_ver.split('.');
    avail_modislock_ver = avail_modislock_ver.split('.');
    current_monitor_ver = current_monitor_ver.split('.');
    avail_monitor_ver = avail_monitor_ver.split('.');

    var modislock_upg = false;
    var monitor_upg = false;

    for(i = 0; i < 3; i++ ){
        if(parseInt(avail_modislock_ver[i]) > parseInt(current_modislock_ver[i])){
            modislock_upg = true;
            break;
        }
    }

    for(i = 0; i < 3; i++ ){
        if(parseInt(avail_monitor_ver[i]) > parseInt(current_monitor_ver[i])){
            monitor_upg = true;
            break;
        }
    }

    $('#btn_admin').prop('disabled', !modislock_upg );
    $('#btn_monitor').prop('disabled', !monitor_upg );
}