from datetime import datetime
from . import db
from sqlalchemy.dialects.mysql import TINYINT, LONGTEXT


class Index(db.Model):
    __tablename__ = 'indexs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    url = db.Column(db.String(255))
    html = db.Column(LONGTEXT)
    status = db.Column(TINYINT(3), default=0)
    dateline = db.Column(db.DateTime(), default=datetime.utcnow)
    lists = db.relationship('List', backref='list', lazy='dynamic')

    def __repr__(self):
        return '<Index %r>' % self.name


class List(db.Model):
    __tablename__ = 'lists'
    id = db.Column(db.Integer, primary_key=True)
    index_id = db.Column(db.Integer, db.ForeignKey('indexs.id'))
    name = db.Column(db.String(64))
    url = db.Column(db.String(255))
    html = db.Column(LONGTEXT)
    status = db.Column(TINYINT(3), default=0)
    dateline = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return '<List %r>' % self.name
