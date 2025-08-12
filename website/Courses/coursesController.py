from flask import Blueprint, render_template, redirect, url_for, request, flash
import MySQLdb.cursors
from .. import mysql
from .coursesModels import (
    GET_COURSES, SEARCH_STUDENTS_NONE, COUNT_STUDENTS_NONE, SEARCH_COURSE_CODE, COUNT_COURSE_CODE,
    DELETE_STUDENT, DELETE_COURSE, DELETE_COLLEGE, UPDATE_COLLEGE, UPDATE_COURSE, UPDATE_STUDENT,
    search_students_by_field
)

controller = Blueprint('courses_controller', __name__)

# Get a list of courses
def get_courses():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(GET_COURSES)
    courses = cursor.fetchall()
    cursor.close()
    return courses


# Route: Search Courses
@controller.route('/search_courses', methods=['POST'])
def search_courses():
    search_field = request.form['search_field']
    search_value = request.form['search_value']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = f"SELECT * FROM courses WHERE {search_field} LIKE %s"
    cursor.execute(query, (f"%{search_value}%",))
    results = cursor.fetchall()
    cursor.close()

    return render_template('courses.html', courses=results)

# Route: Update Courses
@controller.route('/coursesUpdate', methods=['POST'])
def coursesUpdate():
    OLD_COURSE_CODE = request.form['OLD_COURSE_CODE']
    NEW_COURSE_CODE = request.form['NEW_COURSE_CODE']
    COURSE_NAME = request.form['COURSE_NAME']
    COLLEGE_CODE = request.form['COLLEGE_CODE']

    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM courses WHERE COURSE_CODE = %s AND COURSE_CODE != %s", (NEW_COURSE_CODE, OLD_COURSE_CODE))
    exists = cur.fetchone()[0] > 0

    if exists:
        flash("Error: Course code already exists!", category="error")
        return redirect(url_for('courses.coursesPage'))

    cur.execute(UPDATE_COURSE, (NEW_COURSE_CODE, COURSE_NAME, COLLEGE_CODE, OLD_COURSE_CODE))
    mysql.connection.commit()
    cur.close()

    flash("Course updated successfully", category="success")
    return redirect(url_for('courses.coursesPage'))

# Route: Delete Course
@controller.route('/deleteCourse/<course_code>', methods=['POST'])
def deleteCourse(course_code):
    cur = mysql.connection.cursor()
    cur.execute(DELETE_COURSE, (course_code,))
    mysql.connection.commit()
    cur.close()
    flash("Course deleted successfully", category="success")
    return redirect(url_for('courses.coursesPage'))

