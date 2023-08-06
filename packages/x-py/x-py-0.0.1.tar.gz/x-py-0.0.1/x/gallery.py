# -*- coding: utf-8 -*-
"""

"""

import sys
sys.path.append("..")

from models.gallery import Gallery
from models.membership import Account

from sqlalchemy import create_engine, MetaData,\
    Table, Column, Integer, String, ForeignKey

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import datetime
import time
import mysql.connector

import tornado.web


def getHandlers():
    """ """

    handlers = [
        (r"/gallery/list", ListHandler),
        (r"/gallery/form", FormHandler),
        (r"/gallery/detail/([\w+\-]+)", DetailHandler),
    ]

    return handlers

engine = create_engine(
    'mysql+mysqlconnector://test:test@localhost/CW_BigDb', echo=True)


class FormHandler(tornado.web.RequestHandler):
    """ """

    def get(self):
        self.render(
            "gallery/gallery-form.html",
            title="List | Gallery",
            header="form",
            footer="footer text"
        )

    def post(self):
        """ """
        # TODO

        id = self.get_argument('id')
        code = self.get_argument('code')
        name = self.get_argument('name')

        param = Gallery(
            id=id,
            code=code,
            name=name
        )

        Session = sessionmaker(bind=engine)
        session = Session()

        session.add(param)
        session.commit()

        self.write('提交成功!<br/>')
        self.write(name + "<br />")
        self.write('<a href="list">返回列表</a>')
        # self.redirect('list')


class DetailHandler(tornado.web.RequestHandler):
    """ """

    def get(self, id):

        Session = sessionmaker(bind=engine)
        session = Session()

        # first()第一个 all()全部
        result = session.query(Gallery).filter_by(id=id).first()

        self.render(
            "gallery/gallery-detail.html",
            title="Detail | Gallery",
            header="Detail",
            content=result.name + '<br>' +
            result.createdDate.strftime("%Y-%m-%d %X"),
            result=result,
            footer="footer text"
        )


class ListHandler(tornado.web.RequestHandler):
    """ """

    def get(self):

        outString = ''

        cnx = mysql.connector.connect(user='root', password='',
                                      host='127.0.0.1',
                                      database='cw_bigdb')

        cursor = cnx.cursor()

        query = ("SELECT Name, CreatedDate FROM tb_Account "
                 "WHERE CreatedDate BETWEEN %s AND %s")

        hire_start = datetime.date(1970, 1, 1)
        hire_end = datetime.date(1999, 12, 31)

        cursor.execute(query, (hire_start, hire_end))

        for (Name, CreatedDate) in cursor:
            outString += Name + "<br>"
            # print Name
            # print CreatedDate
            # print "{} was hired on {:%d %b %Y}".format(Name, CreatedDate)

        cursor.close()
        cnx.close()

        Session = sessionmaker(bind=engine)
        session = Session()

        # first()第一个 all()全部
        result = session.query(Gallery)

        self.render(
            "gallery/gallery-list.html",
            title="List | Gallery",
            header='',
            list=result,
            footer="footer text"
        )
