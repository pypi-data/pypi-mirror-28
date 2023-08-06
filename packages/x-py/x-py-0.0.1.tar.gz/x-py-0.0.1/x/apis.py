# -*- coding: utf-8 -*-
"""

"""

import tornado.web


class ApiHandler(tornado.web.RequestHandler):
    """ API 请求函数 """

    def get(self, name):
        self.write('api name:' + name)

    def post(self, name):
        self.write('api name:' + name)
