from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login



class Group(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(64), index=True, unique=True)

    users = db.relationship("User", backref="group")

    def __repr__(self):
        return '<Group {}>'.format(self.groupname) 



class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    rolename = db.Column(db.String(64), index=True, unique=True)

    users = db.relationship("User", backref="role")

    def __repr__(self):
        return '<Role {}>'.format(self.rolename) 


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    #roles = db.relationship('Profil', secondary='user_roles')
    #roles = db.Column(db.Integer(), db.ForeignKey('UserRoles.id'))
    #roles = db.relationship("UserRoles", backref = "User")
    #groups = db.relationship('Group', secondary='user_groups')
    tickets = db.relationship("Ticket")
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username) 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Client(db.Model):
    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True)
    clientname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    address = db.Column(db.String(128))
    phone = db.Column(db.String(64))
    tickets = db.relationship("Ticket")
    sales_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Client Name: {}, Email: {}>'.format(self.clientname, self.email) 

class Service(db.Model):
    __tablename__ = "service"

    id = db.Column(db.Integer, primary_key=True)
    servicename = db.Column(db.String(120), index=True, unique=True)
    realcost = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    service_type = db.Column(db.String(64))

    def __repr__(self):
        return '<Service {}>'.format(self.servicename) 

class Equipment(db.Model):
    __tablename__ = "equipment"

    id = db.Column(db.Integer, primary_key=True)
    equip_ref = db.Column(db.String(128), index=True, unique=True)
    brand = db.Column(db.String(64))
    model = db.Column(db.String(128))
    serial = db.Column(db.String(128), unique=False)
    equip_type = db.Column(db.String(64))
    product_num = db.Column(db.String(128))
    tickets = db.relationship("Ticket")
    """valeur calculée"""
    designation = db.Column(db.String(120))
    warranty = db.Column(db.Boolean)
    real_cost = db.Column(db.Numeric(precision=8, asdecimal=False, \
        decimal_return_scale=None))
    
    def __repr__(self):
        return '<Equipment {}>'.format(self.equip_ref) 

    def set_designation(self, brand, model):
        designation = self.brand + self.model


class Ticket(db.Model):
    __tablename__ = "ticket"

    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, index=True, unique=True)
    title = db.Column(db.String(128))
    description = db.Column(db.String(140))
    status = db.Column(db.String(64))
    entry_date = db.Column(db.DateTime, default=datetime.utcnow)
    exit_date = db.Column(db.DateTime, default=datetime.utcnow)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_be_charged = db.Column(db.Boolean)
    #sales_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    #technician_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    invoice_num = db.Column(db.String(120))

    def __repr__(self):
        return '<Ticket {}: {}>'.format(self.ticket_id, self.title)
