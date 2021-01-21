const home_url = 'home/'
const blog_url = 'blog/'

$(document).ready(function () {
    const ajax = {};
    ajax.generateContent = function generateContent (url, elementId) {
        $.get(url, function (data) {
            $(elementId).html(data);
        });
    };

    ajax.showLoading = function showLoading (selector) {
        $(selector).html('<img src="{% static \'base_images/ajax-loading.gif\' %}" height="200" width="200">')
    };

    // generate main-content if location is main page when page is loaded
    if (window.location.pathname === '/') {
        ajax.showLoading('#main-content')
        ajax.generateContent(home_url, '#main-content');
    }
    window.$ajax = ajax;
});
