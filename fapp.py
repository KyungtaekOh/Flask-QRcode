from flask import *
from flask_sqlalchemy import SQLAlchemy
import cv2
import pyzbar.pyzbar as pyzbar
import threading

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fdatabase.sqlite3'

fdatabase = SQLAlchemy(app)
from repository import repository


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/')
def hello_world():
    return render_template('index.html')


class Variable(object):
    def __init__(self):
        self.prev_data = None
        self.barcode_data = None
        self.storename = None
        self.target = None

    def setTarget(self, t):
        self.target = t

    def getTarget(self):
        return self.target

    def setname(self, name):
        self.storename = name

    def getname(self):
        return self.storename

    def setPrev(self, prev):
        self.prev_data = prev

    def setBarcode(self, barc):
        self.barcode_data = barc

    def getPrev(self, **kwargs):
        return self.prev_data

    def getBarcode(self, **kwargs):
        return self.barcode_data


variable = Variable()
from sendMail import mailSender


@app.route('/setting')
def setting():
    return render_template('setting.html')


@app.route('/ajax', methods=['POST'])
def ajax():
    try:
        data = request.get_json(force=True)
        variable.setname(data['name'])
    except Exception as e:
        print(e)
    return jsonify(result="success")


from domain.model import history


@app.route('/ajax2', methods=['POST'])
def query():
    """
    return: 확진 자의 확진일 이후 기록
    """
    try:
        data = request.get_json(force=True)
        pnum = str(data['pnum'])
        date = data['data']
        result = fdatabase.session. \
            query(history.id,
                  history.storeName,
                  history.userPhoneNum,
                  history.userMailAddress,
                  history.dayDateInfo). \
            filter(history.userPhoneNum == pnum,
                   history.dayDateInfo >= date).\
            all()
        print(result)
        """
        return: 동선 겹쳤던 사람들의 정보
        """
        result2 = []
        for ent in result:
            n = str(ent[1])
            d = str(ent[4])
            temp = fdatabase.session. \
                query(history.id,
                      history.storeName,
                      history.userPhoneNum,
                      history.userMailAddress,
                      history.dayDateInfo). \
                filter(history.storeName == n,
                       history.dayDateInfo >= d
                       ).\
                all()
            for i in temp:
                if(i[2] == pnum):
                    continue
                result2.append(i)
        result2 = list(set(result2))  # 중복제거
        variable.setTarget(result2)
    except Exception as e:
        print(e)
    """
    test time :     2020-12-03 00:00:00
    """

    return jsonify(result="success")


@app.route('/ajax3', methods=['POST'])
def mailSend():
    re = "success"
    try:
        data = request.get_json(force=True)
        id = data['id']
        pw = data['pw']
        target = variable.getTarget()
        print('#################')
        for i in target:
            print(i)
        sender = mailSender()
        sender.send_mail(addr=id,
                         subj_layout="코로나 확진자 동선 겹침알림",
                         cont_layout="검사안받으면 3대가 망함")
    except Exception as e:
        print(e)
    return jsonify(result=re)


@app.route('/video')
@app.route('/video/<storename>')
def index(storename=None):
    return render_template('video.html', storename=storename)


@app.route('/camera')
def cam():
    return Response(read_cam(), mimetype='multipart/x-mixed-replace; boundary=mycam')


### CAMERA ###
camera = cv2.VideoCapture(0)  # video device number (/dev/videoX)
if not camera.isOpened():
    raise RuntimeError('Please Check device\'s Camera.')


def read_cam():
    while True:
        ret, img = camera.read()
        if not ret:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        decoded = pyzbar.decode(gray)

        for d in decoded:
            x, y, w, h = d.rect
            variable.setBarcode(d.data.decode("utf-8"))
            barcode_type = d.type
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

            qrTemp = variable.getBarcode().split("|")
            text = '%s (%s)' % (qrTemp[0], barcode_type)
            cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

        if (variable.getBarcode() != variable.getPrev()):
            qrData = variable.getBarcode().split("|")
            print(variable.getname(), qrData)
            variable.setPrev(variable.getBarcode())
            storename = variable.getname()

            dbThread = threading.Thread(target=repository.insertUserData(storename=storename,
                                                                         phoneNum=qrData[0],
                                                                         mailAddress=qrData[1]))
            try:
                dbThread.start()
            except Exception as e:
                print(e)
        # yield Data
        yield (b'--mycam\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'
               + cv2.imencode('.jpg', cv2.cvtColor(img, cv2.IMREAD_COLOR))[1].tobytes()
               + b'\r\n')


def main():
    app.debug = True
    app.run()
    # app.run(host='127.0.0.1', port=5000)


if __name__ == '__main__':
    main()
