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

    // After blog base generated, generate blog page
    window.$ajax.generateContent(blog_url, '#blog-content');
});
