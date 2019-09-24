import os

# Database connections details
connection_host = 'remotemysql.com'
connection_port = 3306
connection_user = 'uHGCP9ySEe'
connection_password = 'YyzSP64QOG'
connection_db = 'uHGCP9ySEe'

# Database connection for Test
connection_host_test = 'remotemysql.com'
connection_port_test = 3306
connection_user_test = 'LXildfOe7a'
connection_password_test = '9YKHZXs1E7'
connection_db_test = 'LXildfOe7a'

# Application url
application_url = 'https://budgetcalculator-thirdproject.herokuapp.com/'


# Secret key
class Config(object):
    SECRET_KEY = os.urandom(12)
