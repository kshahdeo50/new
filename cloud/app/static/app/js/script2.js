$('.modal-toggle').click(function (e) {
   var tab = $(this).data('href');
   $('li > a[href="' + tab + '"]').tab("show");
});
