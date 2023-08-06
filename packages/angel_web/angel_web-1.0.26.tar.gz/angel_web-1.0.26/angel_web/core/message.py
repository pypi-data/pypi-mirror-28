#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         2017-12-21
# @Email        2273337844@qq.com
# @Copyright    © 2017 Lafite93


class Response(object):
    def __init__(self, statusCode, message):
        self.statusCode = statusCode
        self.message = message

    def to_json(self):
        """
        Serilize the response into json string
        """
        res = '{"statusCode":%d, "message":"%s"}'
        return res % (self.statusCode, self.message.replace("\"", "'"))


class FailResponse(Response):
    def __init__(self, message):
        super(FailResponse, self).__init__(CODE_FAIL, message)


CODE_SUCEESS = 200
CODE_FAIL = 300
RESPONSE_SUCCESS = Response(CODE_SUCEESS, "Success").to_json()
RESPONSE_EMPTY_FIELD = Response(CODE_FAIL, "Empty feilds").to_json()
RESPONSE_FAIL = Response(CODE_FAIL, "Fail").to_json()

