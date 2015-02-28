$(document).ready(function() {
    var maxH = 0;

    $(document).foundation();

    $('.b-cards-wrapper').isotope({
        itemSelector: '.b-card',
        layoutMode: 'fitRows'
    });

    $('.b-card').each(function() {
        maxH = $(this).height() > maxH ? $(this).height() : maxH;
    }).height(maxH);

    $('.e-filter-tag').click(function() {
        var filterValue = '';

        $(this).toggleClass('m-active');

        $('.e-filter-tag.m-active').each(function() {
            filterValue += $(this).attr('data-filter');
        });

        $('.b-cards-wrapper').isotope({ filter: filterValue || '*'});

        return false;
    });
 });
