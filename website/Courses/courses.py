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

from .coursesModels import (SELECT_COURSE, SELECT_COLLEGE_CODE, SELECT_COURSES_COUNT, INSERT_COURSES_QUERY, ANOTHER_COURSE_COUNT, Get_Courses, GetColleges, TOTAL, BELOWTOTAL, INSERTCOURSE)

# DB_HOST=localhost
# DB_PORT=3306
# DB_NAME=fssis
# DB_USERNAME=root
# DB_PASSWORD=root
# SECRET_KEY=thisisarandomsecretkey1111
# BOOTSTRAP_SERVE_LOCAL=True
# PIPENV_VENV_IN_PROJECT=1
# CLOUDINARY_URL=cloudinary://419821381875283:Ca2sfgxZK8i4e24vqHPi0ED62Yk@dgmaqsdil

routes = Blueprint('courses', __name__)

#The whole website

import re
from flask import flash, redirect, url_for, render_template, request
import MySQLdb


#The courses table
@routes.route('/courses', methods=['GET', 'POST'])
def coursesPage():
    
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page

    # Get total courses count for pagination
    total_courses = TOTAL()

    # Calculate total pages
    total_pages = max(1, (total_courses + per_page - 1) // per_page)

    # Ensure page is within range
    if page < 1:
        flash("Invalid page number.", "error")
        return redirect(url_for('courses.coursesPage', page=1))
    if page > total_pages:
        flash("Page out of range.", "error")
        return redirect(url_for('courses.coursesPage', page=total_pages))

    if request.method == 'POST':
        COURSE_CODE = request.form['COURSE_CODE']
        COURSE_NAME = request.form['COURSE_NAME']
        COLLEGE_CODE = request.form['COLLEGE_CODE']

        exists = BELOWTOTAL(COURSE_CODE)
        if exists:
            flash("Error: Course code already exists!", category="error")
            return redirect(url_for('courses.coursesPage', page=page))

        INSERTCOURSE(COURSE_CODE, COURSE_NAME, COLLEGE_CODE)

        flash("Course added successfully", category="success")
        return redirect(url_for('courses.coursesPage', page=page))
    
    courvalue = Get_Courses(offset, per_page)
    colvalue = GetColleges()

    return render_template(
        'courses.html',
        courses=courvalue,
        colleges=colvalue,
        current_page=page,
        total_pages=total_pages
    )
