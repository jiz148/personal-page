$(document).ready(function () {
    const ajax = {};
    ajax.generateContent = function generateContent (url) {
        $.get(url, function (data) {
            console.log(data)
            $("#main-content").html(data);
        });
    };
    window.$ajax = ajax;
});
