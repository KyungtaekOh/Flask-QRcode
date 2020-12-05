queryFlag = 0;

function getData() {

    pnum = document.getElementById('pnum');
    date = document.getElementById('date');
    let userPhoneNum = pnumValidation(pnum.value);
    let dateInfo = date.value
    let flag =[0, 0]
    if(userPhoneNum == false){
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
            document.getElementById('mail').style.display='block';
            alert("Please enter an account to send mail");
            queryFlag = 1;
        },
        error: function (request, status, error) {
            alert('Ajax fail!\n' + error);
        }
    });
}

function send(){
    let mid = document.getElementById('aa');
    let id = emailValidation(mid.value);
    let pw = document.getElementById('bb').value;

    if(id == false){
        alert("메일의 형식을 다시 확인해 주세요!");
        mid.value = "";
        return false;
    }

    $.ajax('/ajax3', {
        type: 'POST',
        data: JSON.stringify({'id': id, 'pw':pw}),
        dataType: 'JSON',
        success: function (data) {
            alert("Success mail send!");
            window.location.href = "/";
        },
        error: function (request, status, error) {
            alert('Ajax fail!\n' + error);
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

function cancel(){
    let box = document.getElementById('mail');
    box.style.display = "none";
}

function emailValidation(email) {
    let re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    if (re.test(email)) {
        return email;
    } else {
        return false
    }
}
