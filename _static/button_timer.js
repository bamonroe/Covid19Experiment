//Script for countdown timer
let btnStopTime = -1;
let btnExpirationMessage = "You may now proceed.";
function start_btnTimer(t) {
    if (t == -1) {  // skip timer if participant time limit not set
        return;
    }
    let t_ms = t * 1000;    // Python logs POSIX time in seconds while JS uses milliseconds
    let diff = -1;
    btnStopTime = new Date(Date.now() + t_ms);
    function btn_timer() {
        diff = btnStopTime - Date.now();
        let formatted_time = "NULL";
        if (diff < 0) {
            clearInterval(btn_interval_id);
            formatted_time = btnExpirationMessage;
            $(".otree-btn-next").prop('disabled', false);
        } else {
            diff = (diff / 1000) | 0;   // convert ms to s for easier human consumption
            let d = Math.floor(diff / 86400);
            diff -= d * 86400;
            let h = Math.floor(diff / 3600);
            diff -= h * 3600;
            let m = Math.floor(diff / 60);
            diff -= m * 60;
            let s = Math.floor(diff);
            // formatted_time = d + "d:" + h + 'h:' + m + 'm:' + s + "s";
            formatted_time = "Button will be enabled in " + m + 'm:' + s + "s";
        }
        $("#btn_tmr_msg").html(formatted_time);
    }
    if (btnStopTime - Date.now() > 1){                     // then still time remaining
        var btn_interval_id = setInterval(btn_timer,1000);
    } else {                                            // no time remaining when called; do not start timer
        $(".otree-btn-next").show();
    }
}
$.getScript('https://player.vimeo.com/api/player.js', function()
{
    // disable submit button
    $(".otree-btn-next").prop('disabled', true);
    var iframe = document.querySelector('iframe' );
    var player = new Vimeo.Player(iframe);
    var video_duration = 0;
    player.getDuration().then(function(d) {
        video_duration =  d;
    });
    var player_started = false;
    player.on('play', function() {
        if (player_started === false){
            player_started = true;
            start_btnTimer(video_duration);
        }
    });
});


