from fapp import fdatabase
from domain.model import history


# id = fdatabase.Column(fdatabase.Integer, primary_key=True, autoincrement=True, nullable=False)
# storeName = fdatabase.Column(fdatabase.String(30), nullable=False)
# userPhoneNum = fdatabase.Column(fdatabase.String(30), unique=True, nullable=False)
# userMailAddress = fdatabase.Column(fdatabase.String(30), unique=True, nullable=False)
# dayDateInfo = fdatabase.Column(fdatabase.string(30), nullable=False)

def insertUserData(storename=None, phoneNum=None, mailAddress=None, daydate=None):
    if (storename is None) or (phoneNum is None) or (mailAddress is None) or (daydate is None):
        return print("More need Data")

    userData = history(
        storeName=storename,
        userPhoneNum=phoneNum,
        userMailAddress=mailAddress,
        dayDateInfo=daydate
    )

    try:
        fdatabase.session.add(userData)
        fdatabase.session.commit()
        print("success")
    except Exception as e:
        print(e)

def pageable(per_page, selected_page):
    pagination = history.query.paginate(selected_page, per_page, True)
    return pagination


def find_by_id(id):
    img = history.query.filter_by(id=id).first()
    return img
