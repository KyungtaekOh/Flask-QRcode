from fapp import fdatabase
from domain.model import history
from datetime import datetime
def insertUserData(storename=None, phoneNum=None, mailAddress=None, daydate=None):
    if (storename is None) or (phoneNum is None) or (mailAddress is None):
        return print("More need Data")
    date = datetime.now()

    userData = history(
        storeName=storename,
        userPhoneNum=phoneNum,
        userMailAddress=mailAddress,
        dayDateInfo=date
    )

    try:
        fdatabase.session.add(userData)
        fdatabase.session.commit()
        print("success")
    except Exception as e:
        print(e)

"""
Function Not Use
"""
# def pageable(per_page, selected_page):
#     pagination = history.query.paginate(selected_page, per_page, True)
#     return pagination
#
#
# def find_by_id(id):
#     img = history.query.filter_by(id=id).first()
#     return img
