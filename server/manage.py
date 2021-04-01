# -*- coding: utf-8 -*-
# @Time    : 2020/10/17 12:59 上午
# @Author  : xu.junpeng
from app import create_app
from config import SERVER_PORT
app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=SERVER_PORT)
