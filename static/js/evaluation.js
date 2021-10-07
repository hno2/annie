function addComment(text, location) {
    // post to server
    $.ajax({
        type: "POST",
        url: "/addComment",
        data: {
            markdown: text,
            //cell_id: cell_id, optional
            file: window.location.href.split("/").pop()
        },
        success: function (data) {
            // update comment list
            $(".comments-container").append(data);
            $(".comment-box").val("");
        }
    });

}

$(".comment-box").keyup(function (event) {
    if (event.keyCode == 13) {
        if (this.value.length > 0) { //Disallow empty comments
            addComment($(this).val(), $(this));
        }
    }
});

$(".post").click(function () {
    if ($(".comment-box").val().length > 0) {
        addComment($(".comment-box").val(), $(this));

    }
});


function align_comments() {
    $(".code_cell").each(function (index) {
        block = $(this)
        $("#block-" + index).css({
            position: "absolute",
            top: block.position().top
        });
        $("#block-" + index).removeClass("d-none")
    });
}
$(document).ready(
    align_comments()
)