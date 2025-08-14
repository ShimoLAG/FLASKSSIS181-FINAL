from flask import Blueprint, render_template, redirect, url_for, request, flash
import MySQLdb.cursors
import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api
import math
from dotenv import load_dotenv
load_dotenv()
from .. import mysql
from .studentsModels import (STUDENTS_PAGE, SELECT_COURSES_STUDENTS, CHECK_ID_STUDENTS, STUDENT_GET_COURSES, Get_Students, getCourses, studPages, checkID)

# DB_HOST=localhost
# DB_PORT=3306
# DB_NAME=fssis
# DB_USERNAME=root
# DB_PASSWORD=root
# SECRET_KEY=thisisarandomsecretkey1111
# BOOTSTRAP_SERVE_LOCAL=True
# PIPENV_VENV_IN_PROJECT=1
# CLOUDINARY_URL=cloudinary://419821381875283:Ca2sfgxZK8i4e24vqHPi0ED62Yk@dgmaqsdil

routes = Blueprint('students', __name__)

#The whole website

import re
from flask import flash, redirect, url_for, render_template, request
import MySQLdb

#student table

@routes.route('/', methods=['GET', 'POST'])
def studentsPage():
    

    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    # Get total student count for pagination
    total_students = studPages()

    # Calculate total pages
    total_pages = max(1, (total_students + per_page - 1) // per_page)

    # Ensure page is within range
    if page < 1:
        flash("Invalid page number.", "error")
        return redirect(url_for('students.studentsPage', page=1))
    if page > total_pages:
        flash("Page out of range.", "error")
        return redirect(url_for('students.studentsPage', page=total_pages))

    if request.method == 'POST':
        ID = request.form['ID']
        IMAGE = request.form.get('IMAGE', '').strip()  # Get IMAGE, default to an empty string
        FIRST_NAME = request.form['FIRST_NAME']
        LAST_NAME = request.form['LAST_NAME']
        COURSE_CODE = request.form['COURSE_CODE']
        YEAR = request.form['YEAR']
        GENDER = request.form['GENDER']

        # Set default image if IMAGE is empty
        if not IMAGE:
            IMAGE = '/static/images/default-profile.jpg'  # Ensure this path points to your default image

        checkID(ID,  IMAGE, FIRST_NAME, LAST_NAME, COURSE_CODE, YEAR, GENDER)
        return redirect(url_for('students.studentsPage'))

    # Fetch paginated students and courses
    studvalue = Get_Students(offset, per_page)
    cours = getCourses()

    return render_template(
        'students.html',
        stud=studvalue,
        Cval=cours,
        current_page=page,
        total_pages=total_pages,
        search_field=None,  # No search field for default view
        search_value=None   # No search value for default view
    )