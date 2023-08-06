#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         2017-12-20
# @Email        2273337844@qq.com
# @Copyright    © 2017 Lafite93


if __name__ == "__main__":
    from angel_web import app
    app.serve_forever(debug=True)
