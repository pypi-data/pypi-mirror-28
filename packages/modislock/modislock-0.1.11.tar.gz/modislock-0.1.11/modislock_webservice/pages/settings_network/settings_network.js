/**
 * Created by richard on 11.07.17.
 */

(function(){

    $('#dhcp_mode').checked ? network_enable() : network_disable();
    // Toggle the visibility of the network fields based on switch
    $("#dhcp_mode").change(function(){
        (this.checked) ? network_disable() : network_enable();
    });
})();

/**
 * @brief disables network fields
 */
function network_disable(){
    $("input[id$='address']").prop('disabled', true);
}

/**
 * @brief enables network fields
 */
function network_enable(){
    $("input[id$='address']").prop('disabled', false);
}