$(document).ready(function() {
    var maxH = 0;

    // This MUST BE DONE before initialize foundation and isotope.
    $('.b-card').each(function() {
        maxH = $(this).height() > maxH ? $(this).height() : maxH;
    }).height(maxH);

    $(document).foundation();

    $('.b-cards-wrapper').isotope({
        itemSelector: '.b-card',
        layoutMode: 'fitRows'
    });

    $(document).on('open.fndtn.offcanvas', '[data-offcanvas]', function() {
        $('.left-off-canvas-toggle').addClass('m-active');
        $('.inner-wrap').height($('.b-offcanvas')[0].scrollHeight);
    });

    $(document).on('close.fndtn.offcanvas', '[data-offcanvas]', function() {
        $('.left-off-canvas-toggle').removeClass('m-active');
        $('.inner-wrap').height('auto');
    });


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
