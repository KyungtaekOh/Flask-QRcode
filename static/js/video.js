function sendbyAjax() {
    let name = document.getElementById('storename');
    let flag = 0

    $.ajax('/ajax', {
        type: 'POST',
        data: JSON.stringify({'name': name.value}),
        dataType: 'JSON',
        success: function (data) {
            // to show
            let video = document.getElementById('videoWrapper');
            let page = document.getElementById('name');

            // display none
            let name = document.getElementById('name');
            let store = document.getElementById('storename');
            let btn = document.getElementById('userBut');

            name.style.display = "none";
            store.style.display = "none";
            btn.style.display = "none";

            video.style.display = "block";
            page.style.display = "block";
            page.innerHTML = "Reading QR-Code";

            alert("Start Read QR-Code!");
        },
        error: function (request, status, error) {
            alert('Ajax fail!');
        }
    });

}