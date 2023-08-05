#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         2017-12-21
# @Email        2273337844@qq.com
# @Copyright    © 2017 Lafite93

import json

def row2json(rows):
    """
    Dump result rows of data from db into json
    """
    result = []
    for row in rows:
        item = dict(row.items())
        result.append(item)
    return json.dumps(result)
