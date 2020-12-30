const home_url = 'home/'
const blog_url = 'blog/'

$(document).ready(function () {
    const ajax = {};
    ajax.generateContent = function generateContent (url, elementId) {
        $.get(url, function (data) {
            $(elementId).html(data);
        });
    };

    // generate main-content if location is main page when page is loaded
    if (window.location.pathname === '/') {
        ajax.generateContent(home_url, '#main-content');
    }
    window.$ajax = ajax;
});
