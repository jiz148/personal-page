$(document).ready(function () {
    const blog_url = 'blog/articles/';

    window.$ajax.postArticle = function (url, form) {
        $.post(url, form, function (data) {
            window.$ajax.generateContent(blog_url, '#blog_content');
        });
    };

    // After blog base generated, generate blog page
    window.$ajax.generateContent(blog_url, '#blog-content');
});
