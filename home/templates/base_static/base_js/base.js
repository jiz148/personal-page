const home_url = 'home/'
const blog_url = 'blog/'

$(document).ready(function () {
    const ajax = {};

    ajax.showLoading = function showLoading (selector) {
        $(selector).html('<img src="static/base_images/ajax-loading.gif" height="200" width="200">')
    };

    ajax.generateContent = function generateContent (url, elementId) {
        // show loading first
        ajax.showLoading(elementId)
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
