$(document).ready(function () {
    const blog_url = 'blog/articles/';

    // After blog base generated, generate blog page
    window.$ajax.generateContent(blog_url, '#blog-content');
});
