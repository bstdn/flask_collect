from datetime import datetime
from . import db
from sqlalchemy.dialects.mysql import TINYINT, LONGTEXT
from .collect import create_collect


class Index(db.Model):
    __tablename__ = 'indexs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    url = db.Column(db.String(255))
    html = db.Column(LONGTEXT)
    status = db.Column(TINYINT(3), default=0)
    dateline = db.Column(db.DateTime(), default=datetime.utcnow)
    lists = db.relationship('List', backref='list', lazy='dynamic')

    @staticmethod
    def index_add(name):
        collect = create_collect(name)
        url = collect.base_url
        html = collect.spi.get_source(url)
        if html:
            index_list = collect.spi.get_index_list(html)
            for url, name in index_list:
                real_url = collect.base_url + url
                index = Index.query.filter_by(url=real_url).first()
                if index is None:
                    index = Index(name=name,
                                  url=real_url)
                    db.session.add(index)
                    db.session.commit()
            print('index_add: Success.')
        else:
            print('index_add: Html is None.')

    @staticmethod
    def index_edit(name):
        collect = create_collect(name)
        index_list = Index.query.filter_by(status=0).all()
        if index_list:
            for index in index_list:
                html = collect.spi.get_source(index.url)
                if html:
                    index.html = html
                    index.status = 1
                    db.session.add(index)
                    db.session.commit()
            print('index_edit: Success.')
        else:
            print('index_edit: Index_list is None.')

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

    @staticmethod
    def list_add(name):
        collect = create_collect(name)
        index_list = Index.query.filter_by(status=1).all()
        for index in index_list:
            page_list = collect.spi.get_page_list(index.html)
            for url, name in page_list:
                real_url = collect.base_url + url
                item = List.query.filter_by(url=real_url).first()
                if item is None:
                    item = List(index_id=index.id,
                                name=name,
                                url=real_url)
                    db.session.add(item)
                    db.session.commit()
        print('list_add: Success.')

    @staticmethod
    def list_edit(name):
        collect = create_collect(name)
        item_list = List.query.filter_by(status=0).all()
        if item_list:
            for item in item_list:
                html = collect.spi.get_source(item.url)
                if html:
                    item_html = collect.spi.get_body(html)
                    if item_html:
                        item.html = item_html
                        item.status = 1
                        db.session.add(item)
                        db.session.commit()
            print('list_edit: Success.')
        else:
            print('list_edit: Item_list is None.')

    def __repr__(self):
        return '<List %r>' % self.name
