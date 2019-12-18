import os

class  Development():

    SQLALCHEMY_DATABASE_URI='postgresql://postgres:admin@127.0.0.1:5432/sales_demo'
    SECRET_KEY='fc0413eae060c46c0b2fcff8aaa24ec9'
    DEBUG = True