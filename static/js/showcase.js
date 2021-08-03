$("#video").on("click", function () {
    //Toggle Disable on question textfield
    $("#question").prop("disabled", !$("#question").prop("disabled"));
    $("#videolink").prop("disabled", !$("#videolink").prop("disabled"));
});
$(document).ready(function () {
    $('#tags').select2({
        tags: true,
        tokenSeparators: [',', ';']
    });
});

// Example starter JavaScript for disabling form submissions if there are invalid fields
(() => {
    'use strict';

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation');

    // Loop over them and prevent submission
    Array.prototype.slice.call(forms).forEach((form) => {
        form.addEventListener('submit', (event) => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
})();

$(".pointer").on("click", function () {
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
        $(this).removeClass("pointer").addClass("text-primary");
    });
});