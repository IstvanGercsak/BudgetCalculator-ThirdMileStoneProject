import pymysql
from configuration import *


def set_up_database():
    connection = pymysql.connect(
        host=connection_host_test,
        port=connection_port_test,
        user=connection_user_test,
        passwd=connection_password_test,
        db=connection_db_test
    )

    connection.close()


def tear_down():
    connection = pymysql.connect(
        host=connection_host_test,
        port=connection_port_test,
        user=connection_user_test,
        passwd=connection_password_test,
        db=connection_db_test
    )

    sql_delete_sub_item = "DELETE FROM GROUP_SUB_ITEM"
    sql_delete_group_item = "DELETE FROM GROUP_ITEM"
    sql_delete_users = "DELETE FROM USERS"

    delete_cursor = connection.cursor(pymysql.cursors.DictCursor)
    delete_cursor.execute(sql_delete_sub_item)
    connection.commit()

    delete_cursor.execute(sql_delete_group_item)
    connection.commit()
    delete_cursor.execute(sql_delete_users)
    connection.commit()
    delete_cursor.close()

    connection.close()


# Database testing
def test_db_connection():
    expected_result = None

    connection = pymysql.connect(
        host=connection_host_test,
        port=connection_port_test,
        user=connection_user_test,
        passwd=connection_password_test,
        db=connection_db_test
    )

    test_cursor = connection.cursor(pymysql.cursors.DictCursor)
    test_cursor.execute('SELECT * FROM USERS')
    test_result = test_cursor.fetchone()
    test_cursor.close()
    assert test_result == expected_result

    connection.close()
    tear_down()
