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