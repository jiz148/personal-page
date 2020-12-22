const home_url = 'home/'
$(document).ready(function () {
    const ajax = {};
    ajax.generateContent = function generateContent (url) {
        $.get(url, function (data) {
            $("#main-content").html(data);
        });
    };

    ajax.generateContent(home_url)
    window.$ajax = ajax;
});
