function makeUserUrl() {

    pnum = document.getElementById('pnum');
    mail = document.getElementById('mail');


    let userPhoneNum = pnumValidation(pnum.value);
    let userMailAddress = emailValidation(mail.value);

    let flag =[0, 0]
    if(userPhoneNum == false){1
        pnum.value = "";
        flag[0] = 1;
    }
    if(userMailAddress == false){
        mail.value = "";
        flag[1] = 1;
    }
    if(flag[0]==1 && flag[1]==1){
        alert("휴대전화 번호와 메일을 다시 확인해 주세요!");
        return false;
    }else if(flag[0]==1){
        alert("휴대전화 번호를 다시 확인해 주세요!");
        return false;
    }else if(flag[1]==1){
        alert("메일의 형식을 다시 확인해 주세요!");
        return false;
    }

    // let date = new Date();
    // let dayDateInfo = changeDateFormat(date);

    let userlink = document.getElementById('goQrPage');

    let userUrl = "https://chart.googleapis.com/chart?chs=150x150&cht=qr&chl=" +
        userPhoneNum + "|" + userMailAddress;
    userlink.href = userUrl;
    userlink.style.display = "inline";

    return 0;
}

function emailValidation(email) {
    let re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    if (re.test(email)) {
        return email;
    } else {
        return false
    }
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
