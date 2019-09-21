import os
import pymysql
from flask import Flask, flash, render_template, url_for, redirect, request, session
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = os.urandom(12)

connection_host = 'remotemysql.com'
connection_port = 3306
connection_user = 'uHGCP9ySEe'
connection_password = 'YyzSP64QOG'
connection_db = 'uHGCP9ySEe'


# Start the application
@app.route('/')
def start():
    return render_template("login_page.html")


# Login and drop back if the username-password combination is not right
@app.route('/login', methods=['GET', 'POST'])
def login():
    connection = pymysql.connect(
        host=connection_host,
        port=connection_port,
        user=connection_user,
        passwd=connection_password,
        db=connection_db
    )

    session['username'] = request.form['username']
    given_password = request.form['password']

    user_password_parsing_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql_get_password_from_db = "SELECT PASSWORD as pass FROM USERS WHERE USERNAME = %s"
    user_password_parsing_cursor.execute(sql_get_password_from_db, session['username'])
    result = user_password_parsing_cursor.fetchone()
    user_password_parsing_cursor.close()

    try:
        parsing = (sha256_crypt.verify(given_password, result['pass']))
    except:
        flash('Wrong Username or Password')
        return render_template("login_page.html")

    if sha256_crypt.verify(given_password, result['pass']):
        session['logged_in'] = True
        flash('You were successfully logged in')
        return redirect(url_for("dashboard"))
    else:
        flash('You were not logged in')
        return render_template("login_page.html")


# Arrive to the Dashboard
@app.route('/dashboard')
def dashboard():
    connection = pymysql.connect(
        host=connection_host,
        port=connection_port,
        user=connection_user,
        passwd=connection_password,
        db=connection_db
    )

    username = session['username']

    # Collect the group
    check_existing_group_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql_my_groups = "SELECT * FROM GROUP_ITEM JOIN USERS ON GROUP_ITEM.GROUP_ID = USERS.ID WHERE USERS.USERNAME = %s"
    check_existing_group_cursor.execute(sql_my_groups, username)
    my_groups = check_existing_group_cursor.fetchall()
    check_existing_group_cursor.close()
    # Collect the currency
    get_currency_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql_get_currency = "SELECT DISTINCT CURRENCY FROM USERS WHERE USERNAME = %s"
    get_currency_cursor.execute(sql_get_currency, username)
    currency = get_currency_cursor.fetchone()
    session['currency'] = currency['CURRENCY']
    get_currency_cursor.close()

    # Collect and order my dates
    my_dates_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql_my_dates = "SELECT distinct DATE_YEAR, DATE_MONTH FROM GROUP_ITEM JOIN USERS ON GROUP_ITEM.GROUP_ID = USERS.ID " \
                   "WHERE USERS.USERNAME = %s ORDER BY DATE_YEAR desc, " \
                   "FIELD(DATE_MONTH,'January','February','March','April','May','June','July','August','September','October','November','December') desc"
    my_dates_cursor.execute(sql_my_dates, username)
    my_dates = my_dates_cursor.fetchall()
    my_dates_cursor.close()

    # Sum money
    sum_money_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql_full_sum = "SELECT USERS.USERNAME, SUM(GROUP_SUB_ITEM.VALUE) AS SUM_MONEY FROM USERS JOIN GROUP_ITEM ON " \
                   "USERS.ID = GROUP_ITEM.GROUP_ID JOIN GROUP_SUB_ITEM ON GROUP_ITEM.ID = GROUP_SUB_ITEM.ITEM_ID " \
                   "WHERE USERS.USERNAME = %s GROUP BY USERS.USERNAME"
    sum_money_cursor.execute(sql_full_sum, username)
    sum_money = sum_money_cursor.fetchone()
    sum_money_cursor.close()
    if sum_money is None:
        sum_money_value = 0
    else:
        sum_money_value = sum_money['SUM_MONEY']

    # Saving
    savings_for_user_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql_savings_for_user = "SELECT SUM(GROUP_SUB_ITEM.VALUE) AS SUM_SAVING FROM USERS " \
                           "JOIN GROUP_ITEM ON USERS.ID = GROUP_ITEM.GROUP_ID " \
                           "JOIN GROUP_SUB_ITEM ON GROUP_ITEM.ID = GROUP_SUB_ITEM.ITEM_ID WHERE USERS.USERNAME = %s " \
                           "AND GROUP_ITEM.GROUP_NAME = 'Savings' " \
                           "GROUP BY USERS.USERNAME"
    savings_for_user_cursor.execute(sql_savings_for_user, username)
    sum_saving = savings_for_user_cursor.fetchone()
    savings_for_user_cursor.close()
    if sum_saving is None:
        deduct_saving_sum_value = 0
    else:
        deduct_saving_sum_value = sum_saving['SUM_SAVING']

    # Sum values by group
    group_sum_cursor = connection.cursor(pymysql.cursors.DictCursor)
    row_group_sum = (session['username'])
    sql_group_sum = "SELECT GROUP_ITEM.GROUP_NAME, GROUP_ITEM.DATE_YEAR, GROUP_ITEM.DATE_MONTH, " \
                    "SUM(GROUP_SUB_ITEM.VALUE) AS SUMVALUE " \
                    "FROM GROUP_SUB_ITEM JOIN GROUP_ITEM ON GROUP_SUB_ITEM.ITEM_ID = GROUP_ITEM.ID JOIN USERS " \
                    "ON USERS.ID = GROUP_ITEM.GROUP_ID WHERE USERS.USERNAME = %s GROUP BY GROUP_SUB_ITEM.ITEM_ID"
    group_sum_cursor.execute(sql_group_sum, row_group_sum)
    group_sum_list = group_sum_cursor.fetchall()
    group_sum_cursor.close()

    # Sum money - savings
    sum_money_available = int(sum_money_value) - int(deduct_saving_sum_value)
    sum_money_balance = int(sum_money_value) - int(deduct_saving_sum_value * 2)

    return render_template("dashboard.html", mygroups=my_groups, mydates=my_dates, savings=deduct_saving_sum_value,
                           sumbalance=sum_money_balance, groupsumlist=group_sum_list)


# Search after item
@app.route('/search_result', methods=['POST'])
def search():
    connection = pymysql.connect(
        host=connection_host,
        port=connection_port,
        user=connection_user,
        passwd=connection_password,
        db=connection_db
    )

    search = request.form['search']
    username = session['username']

    search_item_cursor = connection.cursor(pymysql.cursors.DictCursor)
    percent_sign = "%"
    row_search_item = (username, percent_sign, search, percent_sign)
    sql_search_item = "SELECT GROUP_ITEM.GROUP_NAME AS GROUP_NAME, " \
                      "GROUP_ITEM.DATE_YEAR AS DATE_YEAR, " \
                      "GROUP_ITEM.DATE_MONTH AS DATE_MONTH, " \
                      "GROUP_SUB_ITEM.SUB_ITEM_NAME AS SUB_ITEM_NAME, " \
                      "GROUP_SUB_ITEM.VALUE AS VALUE, GROUP_SUB_ITEM.GIVEN_DATE AS GIVEN_DATE " \
                      "FROM GROUP_SUB_ITEM JOIN GROUP_ITEM ON GROUP_SUB_ITEM.ITEM_ID = GROUP_ITEM.ID JOIN USERS " \
                      "ON USERS.ID = GROUP_ITEM.GROUP_ID " \
                      "WHERE USERS.USERNAME = %s AND GROUP_SUB_ITEM.SUB_ITEM_NAME like %s %s %s " \
                      "ORDER BY GROUP_ITEM.DATE_YEAR, GROUP_ITEM.DATE_MONTH DESC"

    search_item_cursor.execute(sql_search_item, row_search_item)
    result = search_item_cursor.fetchall()
    search_item_cursor.close()

    return render_template('search_result.html', search_criteria=search, resultlist=result)


# Sign up
@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')


# Sign in
@app.route('/sign_in', methods=['POST'])
def add_user():
    connection = pymysql.connect(
        host=connection_host,
        port=connection_port,
        user=connection_user,
        passwd=connection_password,
        db=connection_db
    )

    user = request.form['username']
    password = request.form['password']
    currency = request.form['currency']

    sha_password = sha256_crypt.encrypt(password)

    check_username_cursor = connection.cursor(pymysql.cursors.DictCursor)
    row_user = (user, sha_password, currency)
    sql = "SELECT USERNAME FROM USERS WHERE USERNAME = %s"
    check_username_cursor.execute(sql, user)
    result = check_username_cursor.fetchone()
    check_username_cursor.close()

    if result is None:
        insert_user_cursor = connection.cursor()
        sql_insert_user = "INSERT INTO USERS (USERNAME, PASSWORD, CURRENCY) VALUES (%s, %s, %s)"
        insert_user_cursor.execute(sql_insert_user, row_user)
        connection.commit()
        insert_user_cursor.close()
        return render_template("login_page.html")
    else:
        flash('This username is not unique! Please choose another one!')
        return render_template("sign_up.html")


# Add Group
@app.route('/add_group', methods=['POST'])
def add_group():
    connection = pymysql.connect(
        host=connection_host,
        port=connection_port,
        user=connection_user,
        passwd=connection_password,
        db=connection_db
    )

    given_group = request.form['group']
    given_year = request.form['year']
    given_month = request.form['month']

    check_is_available_cursor = connection.cursor(pymysql.cursors.DictCursor)
    row_group = (session['username'], given_group, given_year, given_month)
    sql_check_existing_group = "SELECT USERS.USERNAME, GROUP_ITEM.GROUP_NAME, GROUP_ITEM.DATE_YEAR, GROUP_ITEM.DATE_MONTH " \
                               "FROM GROUP_ITEM JOIN USERS ON " \
                               "GROUP_ITEM.GROUP_ID = USERS.ID " \
                               "WHERE USERS.USERNAME = %s AND GROUP_NAME=%s AND DATE_YEAR=%s AND DATE_MONTH=%s"
    check_is_available_cursor.execute(sql_check_existing_group, row_group)
    result_existing_group = check_is_available_cursor.fetchone()
    check_is_available_cursor.close()

    id_for_group_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql_id_for_user = "SELECT ID FROM USERS WHERE USERNAME=%s"
    id_for_group_cursor.execute(sql_id_for_user, session['username'])
    user_id = id_for_group_cursor.fetchone()
    id_for_group_cursor.close()

    row_for_insert_new_group = (user_id['ID'], given_group, given_year, given_month)

    if result_existing_group is None:
        create_group_cursor = connection.cursor()
        sql_insert_group = "INSERT INTO GROUP_ITEM (GROUP_ID, GROUP_NAME, DATE_YEAR ,DATE_MONTH) " \
                           "VALUES (%s, %s, %s, %s)"
        create_group_cursor.execute(sql_insert_group, row_for_insert_new_group)
        connection.commit()
        create_group_cursor.close()
        flash('New Group Successfully created!')
        return redirect(url_for("dashboard"))
    else:
        flash('You already have the given group for this year and month')
        return redirect(url_for("dashboard"))


# Edit Group
@app.route('/edit_group/<id>/<group_id>', methods=['POST'])
def edit_group(id, group_id):
    connection = pymysql.connect(
        host=connection_host,
        port=connection_port,
        user=connection_user,
        passwd=connection_password,
        db=connection_db
    )

    given_group = request.form['group']
    given_year = request.form['year']
    given_month = request.form['month']

    row_edit_group = (given_group, given_year, given_month, id)
    row_existing_row_check = (given_group, given_year, given_month, group_id)

    # Check whether the actual group-year-month combination is exist or not
    check_existing_group_name_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM GROUP_ITEM WHERE GROUP_NAME=%s AND DATE_YEAR=%s AND DATE_MONTH=%s and GROUP_ID=%s"
    check_existing_group_name_cursor.execute(sql, row_existing_row_check)
    existing_group_name_exist = check_existing_group_name_cursor.fetchone()
    check_existing_group_name_cursor.close()

    # Check whether the group contains sub elements or not
    row_for_sub_item_check = (session['username'], given_group)
    contains_sub_item_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql_contains_sub_item = "SELECT * FROM GROUP_SUB_ITEM JOIN GROUP_ITEM ON GROUP_SUB_ITEM.ITEM_ID = GROUP_ITEM.ID " \
                            "JOIN USERS ON GROUP_ITEM.GROUP_ID = USERS.ID " \
                            "WHERE USERS.USERNAME = %s " \
                            "AND GROUP_ITEM.GROUP_NAME = %s"
    contains_sub_item_cursor.execute(sql_contains_sub_item, row_for_sub_item_check)
    result_existing_sub_item = contains_sub_item_cursor.fetchone()
    print(result_existing_sub_item)
    contains_sub_item_cursor.close()

    if existing_group_name_exist is None:
        if result_existing_sub_item is not None:
            flash("You can not change this group because you have existing Sub item under this group")
            return redirect(url_for("dashboard"))
        update_group_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql_edit_group = "UPDATE GROUP_ITEM SET GROUP_NAME=%s, DATE_YEAR=%s, DATE_MONTH=%s where ID=%s"
        update_group_cursor.execute(sql_edit_group, row_edit_group)
        connection.commit()
        update_group_cursor.close()
        flash('You successfully updated the group')
        return redirect(url_for("dashboard"))
    else:
        flash('This group is already exist with this name-year-month combination!')
        return redirect(url_for("dashboard"))


# Remove Group item
@app.route('/remove_group_item/<id>/<group_id>/<group_name>/<date_year>/<date_month>', methods=['POST'])
def remove_group_item(id, group_id, group_name, date_year, date_month):
    connection = pymysql.connect(
        host=connection_host,
        port=connection_port,
        user=connection_user,
        passwd=connection_password,
        db=connection_db
    )

    check_contains_sub_item_cursor = connection.cursor(pymysql.cursors.DictCursor)
    row_check_existing_sub_item = (group_id, group_name, date_year, date_month)
    sql = "SELECT * FROM GROUP_ITEM JOIN GROUP_SUB_ITEM ON GROUP_ITEM.ID = GROUP_SUB_ITEM.ITEM_ID " \
          "WHERE GROUP_ITEM.GROUP_ID=%s " \
          "AND GROUP_ITEM.GROUP_NAME=%s AND GROUP_ITEM.DATE_YEAR=%s AND GROUP_ITEM.DATE_MONTH=%s"
    check_contains_sub_item_cursor.execute(sql, row_check_existing_sub_item)
    result = check_contains_sub_item_cursor.fetchone()
    check_contains_sub_item_cursor.close()

    if result is None:
        delete_group_item_cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "DELETE FROM GROUP_ITEM WHERE ID = %s"
        delete_group_item_cursor.execute(sql, id)
        connection.commit()
        delete_group_item_cursor.close()
        flash('Group Delete was successful!')
        return redirect(url_for("dashboard"))
    else:
        flash('There is existing sub item under this Group')
        return redirect(url_for("dashboard"))


# View item details
@app.route('/view_details/<groupyear>/<month>/<groupname>')
def view_details(groupyear, month, groupname):
    connection = pymysql.connect(
        host=connection_host,
        port=connection_port,
        user=connection_user,
        passwd=connection_password,
        db=connection_db
    )

    view_date_details_cursor = connection.cursor(pymysql.cursors.DictCursor)
    row_group = (session['username'], groupname, groupyear, month)
    sql_view_the_month = "SELECT GROUP_SUB_ITEM.ID AS SUBID, GROUP_SUB_ITEM.ITEM_ID AS SUBITEMID, " \
                         "GROUP_SUB_ITEM.SUB_ITEM_NAME AS SUB_ITEM_NAME, GROUP_SUB_ITEM.VALUE AS VALUE, " \
                         "GROUP_SUB_ITEM.GIVEN_DATE AS GIVEN_DATE " \
                         "FROM GROUP_ITEM JOIN GROUP_SUB_ITEM ON GROUP_ITEM.ID = GROUP_SUB_ITEM.ITEM_ID JOIN USERS " \
                         "ON USERS.ID = GROUP_ITEM.GROUP_ID WHERE USERS.USERNAME = %s AND GROUP_ITEM.GROUP_NAME = %s " \
                         "AND GROUP_ITEM.DATE_YEAR = %s AND GROUP_ITEM.DATE_MONTH = %s ORDER BY GIVEN_DATE asc"

    view_date_details_cursor.execute(sql_view_the_month, row_group)
    dates_details = view_date_details_cursor.fetchall()
    view_date_details_cursor.close()
    return render_template("view_details.html", groupyear=groupyear, month=month, groupname=groupname,
                           datesdetails=dates_details)


# Add sub item
@app.route('/<groupyear>/<month>/<groupname>/addnewsubitempage', methods=['POST'])
def add_new_sub_item(groupyear, month, groupname):
    connection = pymysql.connect(
        host=connection_host,
        port=connection_port,
        user=connection_user,
        passwd=connection_password,
        db=connection_db
    )

    given_sub_item_name = request.form['subitem']
    given_sub_item_value = request.form['subitemvalue']
    given_date = request.form['date']

    row_for_id = (session['username'], groupname, groupyear, month)

    if groupname == "Bills" or groupname == "Other" or groupname == "Shopping":
        given_sub_item_value = int(given_sub_item_value) * -1

    id_for_group_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql_id_from_group = "SELECT GROUP_ITEM.ID FROM GROUP_ITEM JOIN USERS ON GROUP_ITEM.GROUP_ID = USERS.ID " \
                        "WHERE USERS.USERNAME=%s " \
                        "AND GROUP_ITEM.GROUP_NAME=%s AND GROUP_ITEM.DATE_YEAR=%s AND GROUP_ITEM.DATE_MONTH=%s"
    id_for_group_cursor.execute(sql_id_from_group, row_for_id)
    test = id_for_group_cursor.fetchone()
    id_for_group_cursor.close()

    insert_sub_item_cursor = connection.cursor(pymysql.cursors.DictCursor)
    row_group = (test['ID'], given_sub_item_name, given_sub_item_value, given_date)
    sql_insert_sub_item = "INSERT INTO GROUP_SUB_ITEM(ITEM_ID, SUB_ITEM_NAME, VALUE, GIVEN_DATE) VALUES (%s,%s,%s,%s)"
    insert_sub_item_cursor.execute(sql_insert_sub_item, row_group)
    connection.commit()
    insert_sub_item_cursor.close()
    flash('Sub Item added successfully!')
    return redirect(url_for('view_details', groupyear=groupyear, month=month, groupname=groupname))


# Update sub item
@app.route('/update_sub_item/<id>/<groupname>/<groupyear>/<month>', methods=['POST'])
def update_sub_item(id, groupname, groupyear, month):
    connection = pymysql.connect(
        host=connection_host,
        port=connection_port,
        user=connection_user,
        passwd=connection_password,
        db=connection_db
    )

    given_sub_item_name = request.form['subitem']
    given_sub_item_value = request.form['subitemvalue']
    given_date = request.form['date']

    update_sub_item_cursor = connection.cursor(pymysql.cursors.DictCursor)

    if groupname == "Bills" or groupname == "Other" or groupname == "Shopping":
        given_sub_item_value = int(given_sub_item_value) * -1

    row_to_update = (given_sub_item_name, given_sub_item_value, given_date, id)

    sql = "UPDATE GROUP_SUB_ITEM SET SUB_ITEM_NAME=%s, VALUE=%s, GIVEN_DATE=%s where ID=%s"
    update_sub_item_cursor.execute(sql, row_to_update)
    update_sub_item_cursor.fetchone()
    connection.commit()
    update_sub_item_cursor.close()
    flash('Given Sub Item was Updated!')

    return redirect(url_for('view_details', groupname=groupname, groupyear=groupyear,
                            month=month))


# Delete sub item
@app.route('/delete_sub_item/<id>/<groupname>/<groupyear>/<month>', methods=['POST'])
def delete_sub_item(id, groupname, groupyear, month):
    connection = pymysql.connect(
        host=connection_host,
        port=connection_port,
        user=connection_user,
        passwd=connection_password,
        db=connection_db
    )

    delete_sub_item_cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = "DELETE FROM GROUP_SUB_ITEM WHERE ID=%s"
    delete_sub_item_cursor.execute(sql, id)
    delete_sub_item_cursor.fetchone()
    connection.commit()
    delete_sub_item_cursor.close()
    flash('Given Sub Item was deleted!')
    return redirect(url_for('view_details', groupname=groupname, groupyear=groupyear, month=month))


# Logging out
@app.route("/log_out")
def log_out():
    session.clear()
    flash('You have successfully logged out!')
    return start()


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
