from datetime import datetime
from fapp import fdatabase
'''
TODO:
python
from fapp import db
db.create_all()
'''

class history(fdatabase.Model):
    __tablename__ = 'history'
    id = fdatabase.Column(fdatabase.Integer, primary_key=True, autoincrement=True, nullable=False)
    storeName = fdatabase.Column(fdatabase.String(30), nullable=False)
    userPhoneNum = fdatabase.Column(fdatabase.String(30), nullable=False)
    userMailAddress = fdatabase.Column(fdatabase.String(30), nullable=False)
    dayDateInfo = fdatabase.Column(fdatabase.DATETIME, nullable=False, default=datetime.now())

    # userPhoneNum = fdatabase.Column(fdatabase.String(30), unique=True, nullable=False)
    # userMailAddress = fdatabase.Column(fdatabase.String(30), unique=True, nullable=False)
    # dayDateInfo = fdatabase.Column(fdatabase.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"<User('{self.id}', '{self.storeName}', '{self.userPhoneNum}', '{self.userMailAddress}', '{self.dayDateInfo}')>\n"
