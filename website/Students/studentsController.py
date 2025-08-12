from flask import Blueprint, render_template, redirect, url_for, request, flash
import MySQLdb.cursors
from .. import mysql
from .studentsModels import (
    GET_COURSES, SEARCH_STUDENTS_NONE, COUNT_STUDENTS_NONE, SEARCH_COURSE_CODE, COUNT_COURSE_CODE,
    DELETE_STUDENT, DELETE_COURSE, DELETE_COLLEGE, UPDATE_COLLEGE, UPDATE_COURSE, UPDATE_STUDENT,
    search_students_by_field
)

controller = Blueprint('students_controller', __name__)

# Get a list of courses
def get_courses():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(GET_COURSES)
    courses = cursor.fetchall()
    cursor.close()
    return courses

# Route: Search Students
@controller.route('/search_students', methods=['GET', 'POST'])
def search_students():
    try:
        if request.method == 'POST' or 'search_field' in request.args:
            search_field = request.args.get('search_field', request.form.get('search_field'))
            search_value = request.args.get('search_value', request.form.get('search_value'))

            valid_fields = {'ID', 'FIRST_NAME', 'LAST_NAME', 'COURSE_CODE', 'COURSE_NAME', 'YEAR', 'GENDER'}
            if search_field not in valid_fields:
                flash("Invalid search field", "error")
                return redirect(url_for('students.studentsPage'))

            page = request.args.get('page', 1, type=int)
            per_page = 10
            offset = (page - 1) * per_page

            if search_field in ['COURSE_CODE', 'COURSE_NAME'] and search_value.strip().lower() == 'none':
                query = SEARCH_STUDENTS_NONE
                count_query = COUNT_STUDENTS_NONE
                params = [per_page, offset]
                count_params = []
            elif search_field == 'COURSE_CODE':
                query = SEARCH_COURSE_CODE
                count_query = COUNT_COURSE_CODE
                params = [f"%{search_value}%", f"%{search_value}%", per_page, offset]
                count_params = [f"%{search_value}%", f"%{search_value}%"]
            else:
                query = search_students_by_field(search_field)
                count_query = f"SELECT COUNT(*) AS total FROM students WHERE {search_field} LIKE %s"
                params = [f"%{search_value}%", per_page, offset]
                count_params = [f"%{search_value}%"]

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query, params)
            students = cursor.fetchall()

            cursor.execute(count_query, count_params)
            total_students = cursor.fetchone()['total']
            cursor.close()

            total_pages = (total_students + per_page - 1) // per_page
            courses = get_courses()

            return render_template(
                'students.html',
                stud=students,
                Cval=courses,
                current_page=page,
                total_pages=total_pages,
                search_field=search_field,
                search_value=search_value
            )
        return redirect(url_for('students.studentsPage'))
    except Exception as e:
        import traceback
        traceback.print_exc()
        flash("An error occurred while processing your request.", "error")
        return redirect(url_for('students.studentsPage'))

# Route: Update Students
@controller.route('/studentsUpdate', methods=['POST'])
def studentsUpdate():
    OLD_ID = request.form['OLD_ID']
    NEW_ID = request.form['ID']
    IMAGE = request.form.get('IMAGE', '').strip()
    FIRST_NAME = request.form['FIRST_NAME']
    LAST_NAME = request.form['LAST_NAME']
    COURSE_CODE = request.form['COURSE_CODE']
    YEAR = request.form['YEAR']
    GENDER = request.form['GENDER']

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if not IMAGE:
        cur.execute("SELECT IMAGE FROM students WHERE ID = %s", (OLD_ID,))
        current_image = cur.fetchone()
        IMAGE = current_image['IMAGE'] if current_image and current_image['IMAGE'] else '/static/images/default-profile.jpg'

    if not FIRST_NAME or not LAST_NAME:
        flash("Error: First Name and Last Name cannot be empty.", category="error")
        return redirect(url_for('students.studentsPage'))

    cur.execute("SELECT COUNT(*) AS count FROM students WHERE ID = %s AND ID != %s", (NEW_ID, OLD_ID))
    count = cur.fetchone()['count']

    if count > 0:
        flash("Error: ID already exists. Please use a different ID.", category="error")
        return redirect(url_for('students.studentsPage'))

    cur.execute(UPDATE_STUDENT, (NEW_ID, IMAGE, FIRST_NAME, LAST_NAME, COURSE_CODE, YEAR, GENDER, OLD_ID))
    mysql.connection.commit()
    cur.close()

    flash("Student updated successfully", category="success")
    return redirect(url_for('students.studentsPage'))

# Route: Delete Student
@controller.route('/deleteStudent/<student_id>', methods=['POST'])
def deleteStudent(student_id):
    cur = mysql.connection.cursor()
    cur.execute(DELETE_STUDENT, (student_id,))
    mysql.connection.commit()
    cur.close()
    flash("Student deleted successfully", category="success")
    return redirect(url_for('students.studentsPage'))
