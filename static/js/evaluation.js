function addComment(text, cell_id) {
    // post to server
    $.ajax({
        type: "POST",
        url: "/addComment",
        data: {
            markdown: text,
            cell_id: cell_id,
            file: window.location.href.split("/").pop()
        },
        success: function (data) {
            // update comment list
            $("#comment-list-" + cell_id).append(data);
        }
    });

}

$(".comment-box").keyup(function (event) {
    if (event.keyCode == 13) {
        addComment($(this).val(), $(this).parents()[3].id);
        $(this).val("");
    }
});

$(".post").click(function () {
    addComment($(this).parents()[3].id);
});