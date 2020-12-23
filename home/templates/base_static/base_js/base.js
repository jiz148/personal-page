const home_url = 'home/'

$(document).ready(function () {
    const ajax = {};
    ajax.generateContent = function generateContent (url, elementId) {
        $.get(url, function (data) {
            $(elementId).html(data);
        });
    };

    ajax.generateContent(home_url)
    window.$ajax = ajax;
});
