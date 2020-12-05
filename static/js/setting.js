function getData() {

    // let date = new Date();
    // let dayDateInfo = changeDateFormat(date);
    pnum = document.getElementById('pnum');
    date = document.getElementById('date');
    let userPhoneNum = pnumValidation(pnum.value);
    let dateInfo = date.value
    let flag =[0, 0]
    if(userPhoneNum == false){1
        pnum.value = "";
        flag[0] = 1;
    }
    if(flag[0]==1){
        alert("휴대전화 번호를 다시 확인해 주세요!");
        return false;
    }

    $.ajax('/ajax2', {
        type: 'POST',
        data: JSON.stringify({'pnum': userPhoneNum, 'data':dateInfo}),
        dataType: 'JSON',
        success: function (data) {
            alert("Start success!");
        },
        error: function (request, status, error) {
            alert('Ajax fail!');
            alert(error);
        }
    });
}

function pnumValidation(inputtxt) {
    let phoneno = /^\d{11}$/;
    if(phoneno.test(inputtxt)){
        return inputtxt;
    } else {
        return false;
    }
}

function changeDateFormat(dateObj) {
    let year = dateObj.getFullYear();
    let month = dateObj.getMonth() + 1;
    let date = dateObj.getDate();
    let hour = dateObj.getHours();
    let min = dateObj.getMinutes();

    return year + "-" + month + "-" + date + "-" + hour + "-" + min;
}
