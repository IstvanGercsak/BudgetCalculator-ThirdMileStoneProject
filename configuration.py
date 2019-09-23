import os

# Database connections details
connection_host = 'remotemysql.com'
connection_port = 3306
connection_user = 'uHGCP9ySEe'
connection_password = 'YyzSP64QOG'
connection_db = 'uHGCP9ySEe'


# Secret key
class Config(object):
    SECRET_KEY = os.urandom(12)
