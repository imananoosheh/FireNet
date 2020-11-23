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
        placement: 'top'
    });
    $('#deleteARuleButton').popover({
        trigger: 'hover',
        content: 'Click to DELETE this rule?',
        delay: {"show": 250, "hide": 100},
        placement: 'top'
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

    $(".bagButton").on('click', function () {
        var bagid = $(this).data('bagnameid');
        console.log(bagid);
        var bag_name = document.getElementById(bagid).innerHTML;
        console.log(bag_name);
        appendingHtml = '<form class="d-none" name="bagform" action="/#">' +
            '<input class="d-none" type="text" id="bagname" name="bagname">' +
            '<input class="d-none" type="submit" id="bagnamebutton" value="Submit">' +
            '</form>';
        $(this).after(appendingHtml);
        console.log(appendingHtml)
        document.getElementById('bagname').setAttribute("value",bag_name);
        $('#bagnamebutton').click();
    })
});