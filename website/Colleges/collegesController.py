from flask import Blueprint, render_template, redirect, url_for, request, flash
import MySQLdb.cursors
from .. import mysql
from .collegesModels import (
    GET_COURSES, SEARCH_STUDENTS_NONE, COUNT_STUDENTS_NONE, SEARCH_COURSE_CODE, COUNT_COURSE_CODE,
    DELETE_STUDENT, DELETE_COURSE, DELETE_COLLEGE, UPDATE_COLLEGE, UPDATE_COURSE, UPDATE_STUDENT,
    search_students_by_field
)

controller = Blueprint('colleges_controller', __name__)



# Route: Search Colleges
@controller.route('/search_colleges', methods=['POST'])
def search_colleges():
    search_field = request.form['search_field']
    search_value = request.form['search_value']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = f"SELECT * FROM colleges WHERE {search_field} LIKE %s"
    cursor.execute(query, (f"%{search_value}%",))
    results = cursor.fetchall()
    cursor.close()

    return render_template('colleges.html', colleges=results)

# Route: Update Colleges
@controller.route('/collegesUpdate', methods=['POST'])
def collegesUpdate():
    OLD_COLLEGE_CODE = request.form['OLD_COLLEGE_CODE']
    NEW_COLLEGE_CODE = request.form['NEW_COLLEGE_CODE']
    COLLEGE_NAME = request.form['COLLEGE_NAME']

    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM colleges WHERE COLLEGE_CODE = %s AND COLLEGE_CODE != %s", (NEW_COLLEGE_CODE, OLD_COLLEGE_CODE))
    exists = cur.fetchone()[0] > 0

    if exists:
        flash("Error: College code already exists!", category="error")
        return redirect(url_for('colleges.collegesPage'))

    cur.execute(UPDATE_COLLEGE, (NEW_COLLEGE_CODE, COLLEGE_NAME, OLD_COLLEGE_CODE))
    mysql.connection.commit()
    cur.close()

    flash("College updated successfully", category="success")
    return redirect(url_for('colleges.collegesPage'))

# Route: Delete College
@controller.route('/deleteCollege/<college_code>', methods=['POST'])
def deleteCollege(college_code):
    cur = mysql.connection.cursor()
    cur.execute(DELETE_COLLEGE, (college_code,))
    mysql.connection.commit()
    cur.close()
    flash("College deleted successfully", category="success")
    return redirect(url_for('colleges.collegesPage'))