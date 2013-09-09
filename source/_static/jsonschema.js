$(function(){
    $(document).on('shown', 'a[data-toggle="tab"]', function (e) {
        alert($(e.target).attr('href'));
    })
})
