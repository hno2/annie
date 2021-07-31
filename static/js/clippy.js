function getBotResponse() {
    var userText = $('#message').val();
    var userHtml = '<div class="col-10 card "> <div class="card-body">' + userText + '</div></div><div class="col-1"><img src="/img/user.svg" alt="User" height="57px"></div>'
    $('#message').val('');
    $("#chatbox").append(userHtml);

    var botText = "Good"
    var botHtml = '<div class="col-1"><img src="img/clippy.svg" class="clippy" alt="Clippy" height="60px"></div><div class="col-10 card text-white bg-primary"><div class="card-body">' + botText + '</div></div>';

}

$("#message").keypress(function (e) { // ON Enter
    if (e.which == 13) {
        getBotResponse();
    }
});