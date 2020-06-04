from marshmallow import fields, Schema
import pytz
from . import db, bcrypt
import datetime

tz = pytz.timezone('Asia/Jakarta')
ct = datetime.datetime.now(tz=tz)
jakarta_now = ct.strftime('%Y-%m-%d %H:%m:%S')


class UsersModel(db.Model):
    """
        User Model class
    """
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = self.__generate_hash(password)
        self.created_at = jakarta_now
        self.modified_at = jakarta_now

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def get_all_users():
        return UsersModel.query.all()

    @staticmethod
    def get_one_user(id):
        return UsersModel.query.get(id)

    @staticmethod
    def get_user_by_username(value):
        return UsersModel.query.filter_by(username=value).first()

    def __repr(self):
        return '<id {}>'.format(self.id)


class UsersSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)