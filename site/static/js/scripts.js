$(document).ready(function() {
    $(document).foundation();

    $('#cards-wrapper').isotope({
        itemSelector: '.card',
        layoutMode: 'fitRows'
    });

    $('#filters').on( 'click', 'button', function() {
        var filterValue = $(this).attr('data-filter');

        $('#cards-wrapper').isotope({ filter: filterValue });

        return false;
    });
 });
