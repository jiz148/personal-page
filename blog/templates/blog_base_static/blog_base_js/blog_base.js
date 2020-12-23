$(document).ready(function () {
    const blog_url = 'blog/articles/'

    window.$ajax.generateContent(blog_url, '#blog-content');
});
