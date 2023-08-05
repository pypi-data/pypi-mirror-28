/**
 * Created by richard on 11.07.17.
 */

(function(){
    $("#relay_1_delay").TouchSpin({
        min: 500,
        max: 5000,
        step: 100,
        decimals: 0,
        postfix: 'ms'
    });

    $("#relay_2_delay").TouchSpin({
        min: 500,
        max: 5000,
        step: 100,
        decimals: 0,
        postfix: 'ms'
    });
})();