$(document).ready(function () {
    const blog_url = 'blog/articles/';
    window.$ajax.favArticle = function(url, article_id){
        $.post(url, {}, function () {
            $("#unfavorite_" + article_id).toggle();
            $("#favorite_" + article_id).toggle();
        }).fail(function(xhr) {
            alert('Url failed with ' + xhr.status + ' ' + url)
        });
    }
    $('#article-search-form').submit(function (event){
        // prevent Default event of form
        event.preventDefault();

        $.ajax({
            method: $(this).attr('method'),
            url: $(this).attr('action'),
            data: {
                search: $('#search-str').val(),
            },
            success: function (res){
                // generate main-content first, then blog-content
                $('#blog-content').html(res);
            },
        })
    });

    // After blog base generated, generate blog page
    window.$ajax.generateContent(blog_url, '#blog-content');
});
