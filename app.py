import os

import pymysql
from flask import Flask, flash, render_template, url_for, redirect, request, session
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = os.urandom(12)

connection = pymysql.connect(
    host='remotemysql.com',
    port=3306,
    user='uHGCP9ySEe',
    passwd='YyzSP64QOG',
    db='uHGCP9ySEe'
)

insertuser = connection.cursor()
existinggroupcursor = connection.cursor(pymysql.cursors.DictCursor)
creategroupcursor = connection.cursor()
mydatescursor = connection.cursor(pymysql.cursors.DictCursor)
viewdatedetails = connection.cursor(pymysql.cursors.DictCursor)
insertsubitem = connection.cursor(pymysql.cursors.DictCursor)
userpasswordparsing = connection.cursor(pymysql.cursors.DictCursor)
chekisavailable = connection.cursor(pymysql.cursors.DictCursor)
idforgroup = connection.cursor(pymysql.cursors.DictCursor)
deletesubitemcursor = connection.cursor(pymysql.cursors.DictCursor)
checkusername = connection.cursor(pymysql.cursors.DictCursor)
summoneycursor = connection.cursor(pymysql.cursors.DictCursor)
groupsum = connection.cursor(pymysql.cursors.DictCursor)
updatesubitemcursor = connection.cursor(pymysql.cursors.DictCursor)
updategroupcursor = connection.cursor(pymysql.cursors.DictCursor)
checkexistinggroupname = connection.cursor(pymysql.cursors.DictCursor)
checkcontainssubitems = connection.cursor(pymysql.cursors.DictCursor)
deletegroupitem = connection.cursor(pymysql.cursors.DictCursor)
searchitemcursor = connection.cursor(pymysql.cursors.DictCursor)


# Start the application
@app.route('/')
def start():
    return render_template("loginPage.html")


# Login and drop back if the username-password combination is not right
@app.route('/login', methods=['GET', 'POST'])
def login():
    session['username'] = request.form['username']
    givenpassword = request.form['password']

    getpasswordfromdbsql = "SELECT " \
                           "PASSWORD as pass " \
                           "FROM " \
                           "USERS " \
                           "WHERE USERNAME = %s"
    userpasswordparsing.execute(getpasswordfromdbsql, session['username'])
    result = userpasswordparsing.fetchone()

    try:
        parsing = (sha256_crypt.verify(givenpassword, result['pass']))
    except:
        flash('Wrong Username or Password')
        return render_template("loginPage.html")

    if (sha256_crypt.verify(givenpassword, result['pass'])):
        session['logged_in'] = True
        flash('You were successfully logged in')
        return redirect(url_for("dashboard"))
    else:
        flash('You weren`t logged in')
        return render_template("loginPage.html")


# Arrive to the Dashboard
@app.route('/dashboard')
def dashboard():
    username = session['username']

    sqlmygroups = "SELECT " \
                  "* " \
                  "FROM " \
                  "GROUP_ITEM JOIN USERS " \
                  "ON " \
                  "GROUP_ITEM.GROUP_ID = USERS.ID " \
                  "WHERE USERS.USERNAME = %s"
    existinggroupcursor.execute(sqlmygroups, username)
    mygroups = existinggroupcursor.fetchall()

    sqlmydates = "SELECT " \
                 "distinct DATE_YEAR, " \
                 "DATE_MONTH " \
                 "FROM " \
                 "GROUP_ITEM JOIN USERS " \
                 "ON " \
                 "GROUP_ITEM.GROUP_ID = USERS.ID " \
                 "WHERE USERS.USERNAME = %s " \
                 "ORDER BY DATE_YEAR desc, " \
                 "FIELD(DATE_MONTH,'January','February','March','April','May','June','July','August','September','October','November','December') desc"
    mydatescursor.execute(sqlmydates, username)
    mydates = mydatescursor.fetchall()

    sqlfullsum = "SELECT " \
                 "USERS.USERNAME, " \
                 "SUM(GROUP_SUB_ITEM.VALUE) AS sum_money " \
                 "FROM USERS JOIN GROUP_ITEM " \
                 "ON " \
                 "USERS.ID = GROUP_ITEM.GROUP_ID JOIN GROUP_SUB_ITEM " \
                 "ON " \
                 "GROUP_ITEM.ID = GROUP_SUB_ITEM.ITEM_ID " \
                 "WHERE USERS.USERNAME = %s " \
                 "GROUP BY USERS.USERNAME"
    summoneycursor.execute(sqlfullsum, username)
    summoney = summoneycursor.fetchone()

    rowgroupsum = (session['username'])
    groupsumsql = "SELECT GROUP_ITEM.GROUP_NAME, GROUP_ITEM.DATE_YEAR, GROUP_ITEM.DATE_MONTH, SUM(GROUP_SUB_ITEM.VALUE) AS SUMVALUE FROM GROUP_SUB_ITEM JOIN GROUP_ITEM ON GROUP_SUB_ITEM.ITEM_ID = GROUP_ITEM.ID JOIN USERS ON USERS.ID = GROUP_ITEM.GROUP_ID WHERE USERS.USERNAME = %s GROUP BY GROUP_SUB_ITEM.ITEM_ID"

    groupsum.execute(groupsumsql, rowgroupsum)
    groupsumlist = groupsum.fetchall()

    return render_template("dashboard.html", mygroups=mygroups, mydates=mydates, summoney=summoney,
                           groupsumlist=groupsumlist)


@app.route('/searchresult', methods=['POST'])
def search():
    search = request.form['search']
    username = session['username']

    # Result should be Date-Groups-Date-Item-Value-Expanse date
    percentsign = "%"
    rowsearchitem = (username, percentsign, search, percentsign)
    sqlsearchitem = "SELECT GROUP_ITEM.GROUP_NAME, GROUP_ITEM.DATE_YEAR, GROUP_ITEM.DATE_MONTH, GROUP_SUB_ITEM.SUB_ITEM_NAME, GROUP_SUB_ITEM.VALUE, GROUP_SUB_ITEM.GIVEN_DATE FROM GROUP_SUB_ITEM JOIN GROUP_ITEM ON GROUP_SUB_ITEM.ITEM_ID = GROUP_ITEM.ID JOIN USERS ON USERS.ID = GROUP_ITEM.GROUP_ID WHERE USERS.USERNAME = %s AND GROUP_SUB_ITEM.SUB_ITEM_NAME like %s %s %s"

    searchitemcursor.execute(sqlsearchitem, rowsearchitem)
    result = searchitemcursor.fetchall()
    print(result)

    return render_template('searchresult.html', search_criteria=search)


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signin', methods=['POST'])
def adduser():
    user = request.form['username']
    password = request.form['password']

    shapassword = sha256_crypt.encrypt(password)

    rowuser = (user, shapassword)
    sql = "SELECT " \
          "USERNAME " \
          "FROM " \
          "USERS " \
          "WHERE USERNAME = %s"
    checkusername.execute(sql, user)
    result = checkusername.fetchone()
    if (result == None):
        sqlinsertuser = "INSERT INTO " \
                        "USERS (USERNAME, PASSWORD) " \
                        "VALUES " \
                        "(%s, %s)"
        insertuser.execute(sqlinsertuser, rowuser)
        connection.commit()
        return render_template("loginPage.html")
    else:
        flash('This username is not unique! Please choose another one!')
        return render_template("signup.html")


# Add Group
@app.route('/addgroup', methods=['POST'])
def addgroup():
    givengroup = request.form['group']
    givenyear = request.form['year']
    givenmonth = request.form['month']

    rowgroup = (session['username'], givengroup, givenyear, givenmonth)

    sql = "SELECT " \
          "USERS.USERNAME, " \
          "GROUP_ITEM.GROUP_NAME, " \
          "GROUP_ITEM.DATE_YEAR, " \
          "GROUP_ITEM.DATE_MONTH " \
          "FROM " \
          "GROUP_ITEM JOIN USERS " \
          "ON " \
          "GROUP_ITEM.GROUP_ID = USERS.ID " \
          "WHERE USERS.USERNAME = %s " \
          "AND GROUP_NAME=%s " \
          "AND DATE_YEAR=%s " \
          "AND DATE_MONTH=%s"
    chekisavailable.execute(sql, rowgroup)
    result = chekisavailable.fetchone()

    sqlidforuser = "SELECT " \
                   "ID " \
                   "FROM " \
                   "USERS " \
                   "WHERE USERNAME=%s"
    idforgroup.execute(sqlidforuser, session['username'])
    userID = idforgroup.fetchone()

    rowforinsertnewgroup = (userID['ID'], givengroup, givenyear, givenmonth)

    if (result == None):
        sqlinsertgroup = "INSERT INTO " \
                         "GROUP_ITEM " \
                         "(GROUP_ID, GROUP_NAME, DATE_YEAR ,DATE_MONTH) " \
                         "VALUES " \
                         "(%s, %s, %s, %s)"
        creategroupcursor.execute(sqlinsertgroup, rowforinsertnewgroup)
        connection.commit()
        flash('New Group Successfully created!')
        return redirect(url_for("dashboard"))
    else:
        flash('You already have the given group for this year and month')
        return redirect(url_for("dashboard"))


# Edit Group
@app.route('/editgroup/<id>/<group_id>', methods=['POST'])
def editgroup(id, group_id):
    givengroup = request.form['group']
    givenyear = request.form['year']
    givenmonth = request.form['month']

    roweditgroup = (givengroup, givenyear, givenmonth, id)
    rowexistingrowcheck = (givengroup, givenyear, givenmonth, group_id)

    sql = "SELECT * FROM GROUP_ITEM WHERE GROUP_NAME=%s AND DATE_YEAR=%s AND DATE_MONTH=%s and GROUP_ID=%s"
    checkexistinggroupname.execute(sql, rowexistingrowcheck)
    connection.commit()
    result = checkexistinggroupname.fetchone()

    if (result == None):
        sqleditgroup = "UPDATE GROUP_ITEM SET GROUP_NAME=%s, DATE_YEAR=%s, DATE_MONTH=%s where ID=%s"
        updategroupcursor.execute(sqleditgroup, roweditgroup)
        connection.commit()
        flash('You successfully updated the group')
        return redirect(url_for("dashboard"))
    else:
        flash('tHIS GROUP IS ALREADY EXIST WITH THIS NAME, YEAR AND MONTH COMBINATION ')
        return redirect(url_for("dashboard"))


# Remove Group item
@app.route('/removegroupitem/<id>/<group_id>/<group_name>/<date_year>/<date_month>', methods=['POST'])
def removegroupitem(id, group_id, group_name, date_year, date_month):
    rowcheckexistingsubitem = (group_id, group_name, date_year, date_month)
    sql = "SELECT * FROM GROUP_ITEM JOIN GROUP_SUB_ITEM ON GROUP_ITEM.ID = GROUP_SUB_ITEM.ITEM_ID WHERE GROUP_ITEM.GROUP_ID=%s AND GROUP_ITEM.GROUP_NAME=%s AND GROUP_ITEM.DATE_YEAR=%s AND GROUP_ITEM.DATE_MONTH=%s"
    checkcontainssubitems.execute(sql, rowcheckexistingsubitem)
    connection.commit()
    result = checkcontainssubitems.fetchone()

    if (result == None):
        sql = "DELETE FROM GROUP_ITEM WHERE ID = %s"
        deletegroupitem.execute(sql, id)
        connection.commit()
        flash('Group Delete was successful!')
        return redirect(url_for("dashboard"))
    else:
        flash('There is existing sub item under this Group')
        return redirect(url_for("dashboard"))


@app.route('/viewdetails/<groupyear>/<month>/<groupname>')
def viewdetails(groupyear, month, groupname):
    rowgroup = (session['username'], groupname, groupyear, month)
    sqlviewthemonth = "SELECT " \
                      "GROUP_SUB_ITEM.ID AS SUBID, GROUP_SUB_ITEM.ITEM_ID AS SUBITEMID, " \
                      "GROUP_SUB_ITEM.SUB_ITEM_NAME AS SUB_ITEM_NAME, " \
                      "GROUP_SUB_ITEM.VALUE AS VALUE, " \
                      "GROUP_SUB_ITEM.GIVEN_DATE AS GIVEN_DATE " \
                      "FROM " \
                      "GROUP_ITEM JOIN GROUP_SUB_ITEM " \
                      "ON " \
                      "GROUP_ITEM.ID = GROUP_SUB_ITEM.ITEM_ID JOIN USERS " \
                      "ON " \
                      "USERS.ID = GROUP_ITEM.GROUP_ID " \
                      "WHERE USERS.USERNAME = %s " \
                      "AND GROUP_ITEM.GROUP_NAME = %s " \
                      "AND GROUP_ITEM.DATE_YEAR = %s " \
                      "AND GROUP_ITEM.DATE_MONTH = %s " \
                      "ORDER BY GIVEN_DATE asc"

    viewdatedetails.execute(sqlviewthemonth, rowgroup)
    datesdetails = viewdatedetails.fetchall()
    return render_template("viewdetails.html", groupyear=groupyear, month=month, groupname=groupname,
                           datesdetails=datesdetails)


# Add sub item
@app.route('/<groupyear>/<month>/<groupname>/addnewsubitempage', methods=['POST'])
def addnewsubitem(groupyear, month, groupname):
    givensubitemname = request.form['subitem']
    givensubitemvalue = request.form['subitemvalue']
    givendate = request.form['date']

    rowforid = (session['username'], groupname, groupyear, month)
    sqlidfromgroup = "SELECT " \
                     "GROUP_ITEM.ID " \
                     "FROM " \
                     "GROUP_ITEM JOIN USERS " \
                     "ON " \
                     "GROUP_ITEM.GROUP_ID = USERS.ID " \
                     "WHERE USERS.USERNAME=%s " \
                     "AND GROUP_ITEM.GROUP_NAME=%s " \
                     "AND GROUP_ITEM.DATE_YEAR=%s " \
                     "AND GROUP_ITEM.DATE_MONTH=%s"
    idforgroup.execute(sqlidfromgroup, rowforid)
    test = idforgroup.fetchone()

    rowgroup = (test['ID'], givensubitemname, givensubitemvalue, givendate)
    sqlinsertsubitem = "INSERT " \
                       "INTO GROUP_SUB_ITEM(ITEM_ID, " \
                       "SUB_ITEM_NAME, VALUE, GIVEN_DATE) " \
                       "VALUES (%s,%s,%s,%s)"
    insertsubitem.execute(sqlinsertsubitem, rowgroup)
    connection.commit()
    flash('Sub Item added successfully!')
    return redirect(url_for('viewdetails', groupyear=groupyear, month=month, groupname=groupname))


# Update sub item
@app.route('/updateupdatesubitem/<id>/<groupname>/<groupyear>/<month>', methods=['POST'])
def updateupdatesubitem(id, groupname, groupyear, month):
    givensubitemname = request.form['subitem']
    givensubitemvalue = request.form['subitemvalue']
    givendate = request.form['date']
    rowtoupdate = (givensubitemname, givensubitemvalue, givendate, id)
    sql = "UPDATE GROUP_SUB_ITEM SET SUB_ITEM_NAME=%s, VALUE=%s, GIVEN_DATE=%s where ID=%s"
    updatesubitemcursor.execute(sql, rowtoupdate)
    updatesubitemcursor.fetchone()
    connection.commit()
    flash('Given Sub Item was Updated!')
    return redirect(url_for('viewdetails', groupname=groupname, groupyear=groupyear,
                            month=month))


# Delete sub item
@app.route('/deletesubitem/<id>/<groupname>/<groupyear>/<month>', methods=['POST'])
def deletesubitem(id, groupname, groupyear, month):
    sql = "DELETE " \
          "FROM " \
          "GROUP_SUB_ITEM " \
          "WHERE ID=%s"
    deletesubitemcursor.execute(sql, id)
    deletesubitemcursor.fetchone()
    connection.commit()
    flash('Given Sub Item was deleted!')
    return redirect(url_for('viewdetails', groupname=groupname, groupyear=groupyear, month=month))


@app.route("/logout")
def logout():
    session.clear()
    flash('You have successfully logged out!')
    return start()


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
