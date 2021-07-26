/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
    document.getElementById("sidenav").setAttribute("data-hidden", "false");
    document.getElementById("content").style.marginLeft = "240px";
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav() {
    document.getElementById("sidenav").setAttribute("data-hidden", "true");
    document.getElementById("content").style.marginLeft = "0";
}
$("#sidenav-toggle").on("click", function () {
    if (document.getElementById("sidenav").getAttribute("data-hidden") == "false") {
        closeNav()
    } else {
        openNav()
    }
})

function align_comments() {
    /*For every pre (TODO:check is not empty*/
    $(".CodeMirror").each(function (index) {
        block = $(this)
        $("#block-" + index).css({
            position: "absolute",
            top: block.position().top
        })
    });
}
$(document).ready(
    align_comments()
)

$(".upvote").on("click", function () {
    var new_value = Number($(".score", this).text()) + 1;
    $(".score", this).text(new_value);
    $.ajax({
        context: this,
        type: "POST",
        url: "/upvote",
        data: {
            showcase_id: $(this).parents(".card").attr("id")
        }
    }).done(function () {
        // remove click listener to prevent multiple clicks
        $(this).off("click");
    });
});