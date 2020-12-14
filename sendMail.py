from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

class mailSender(object):

    def __init__(self):
        # SMTP 접속을 위한 서버, 계정 설정
        self.SMTP_SERVER = "smtp.gmail.com"
        self.SMTP_PORT = 465

        # 보내는 메일 계정
        self.SMTP_USER = "address@example.com"
        self.SMTP_PASSWORD = "pass"


    # 이메일 유효성 검사 함수
    def is_valid(self, addr):
        import re
        if re.match('(^[a-zA-Z-0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', addr):
            return True
        else:
            return False


    # 이메일 보내기 함수
    def send_mail(self,
                  addr=None,
                  subj_layout="Test",
                  cont_layout="검사안받으면 3대가 망함",
                  attachment=None):
        if not self.is_valid(addr):
            print("Wrong email: " + addr)
            return

        # 텍스트 파일
        msg = MIMEMultipart("alternative")
        # 첨부파일이 있는 경우 mixed로 multipart 생성
        if attachment:
            msg = MIMEMultipart('mixed')
        msg["From"] = self.SMTP_USER
        msg["To"] = addr
        msg["Subject"] = subj_layout
        contents = cont_layout
        text = MIMEText(_text=contents, _charset="utf-8")
        msg.attach(text)
        # 첨부파일이 있으면
        if attachment:
            from email.mime.base import MIMEBase
            from email import encoders
            file_data = MIMEBase("application", "octect-stream")
            file_data.set_payload(open(attachment, "rb").read())
            encoders.encode_base64(file_data)
            import os
            filename = os.path.basename(attachment)
            file_data.add_header("Content-Disposition", 'attachment', filename=('UTF-8', '', filename))
            msg.attach(file_data)
        # smtp로 접속할 서버 정보를 가진 클래스변수 생성
        smtp = smtplib.SMTP_SSL(self.SMTP_SERVER, self.SMTP_PORT)
        # 해당 서버로 로그인
        smtp.login(self.SMTP_USER, self.SMTP_PASSWORD)
        # 메일 발송
        smtp.sendmail(self.SMTP_USER, addr, msg.as_string())
        # 닫기
        smtp.close()


# if __name__ == '__main__':
#     send = mailSender()
#     send.send_mail()
