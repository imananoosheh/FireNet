// var navBar = document.getElementById("mainNavbar")
// var navButtons = navBar.getElementsByClassName("nav-link")

// function mouseoverFunction() {
//     var object = this.options[this.selectedIndex].value;
//     object.classList.add("active");
// }
//
// function mouseoutFunction() {
//     var object = this.options[this.selectedIndex].value;
//     object.classList.remove("active");
// }
//
// for (var i = 0; i < navButtons.length; i++) {
//     navButtons[i].addEventListener("mouseover", function() {
//         this.classList.add("active");
//     }, false);
//     navButtons[i].addEventListener("mouseout", function() {
//         this.classList.remove("active");
//     }, false);
// }

$(function () {
    // Sidebar toggle behavior
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar, #content').toggleClass('active');
    });
});

// $("#sidebarCollapse").popover({trigger: "hover", delay: {"show": 250, "hide": 100}, placement: "right"});

// jQuery("document").ready(function ($) {
//     $(".clickable-row").click(function () {
//         window.location = $(this).data("href");
//         $(this).toggleClass('active');
//         if ($(this).hasClass('active')) {
//             $(this).append("<div id='current_editing' class='col-1 d-table text-center'><span id='current_arrow' class='material-icons'>east</span></div>");
//         } else {
//             $('#current_editing').remove();
//         }
//     });
// });


jQuery(document).ready(function () {

    $('#addBagButton').popover({
        trigger: 'hover',
        title: 'Add a rule',
        content: 'Click to add a rule (last 3 fields are optional)',
        delay: {"show": 250, "hide": 100},
        placement: 'right'
    });
    $('#cancelModyfiyARule').popover({
        trigger: 'hover',
        content: 'Cancel / Close',
        delay: {"show": 250, "hide": 100},
        placement: 'left'
    });
    $('#editModyfiyARule').popover({
        trigger: 'hover',
        content: 'Cancel / Close',
        delay: {"show": 250, "hide": 100},
        placement: 'left'
    });
    $(".clickable-row").click(function () {
        window.location = $(this).data("href");
        $(this).toggleClass('active');
        if ($(this).hasClass('active')) {
            $(this).append("<div id='current_editing' class='col-1 d-table text-center'><span id='current_arrow' class='material-icons'>east</span></div>");
        } else {
            $('#current_editing').remove();
        }
    });
});