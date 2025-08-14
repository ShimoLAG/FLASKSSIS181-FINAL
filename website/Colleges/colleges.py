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
from .collegesModels import (SELECT_COUNT_COLLEGES, INSERT_INTO_COLLEGE, COUNT_COLLEGE, COLLEGE_QUERY_FOUR)


import re
from flask import flash, redirect, url_for, render_template, request
import MySQLdb

routes = Blueprint('colleges', __name__)

#The college table
@routes.route('/colleges', methods=['GET', 'POST'])
def collegesPage():
    PER_PAGE = 5  # number of colleges per page

    if request.method == 'POST':
        COLLEGE_CODE = request.form['COLLEGE_CODE']
        COLLEGE_NAME = request.form['COLLEGE_NAME']
        
        # Check if college code exists
        cursor = mysql.connection.cursor()
        cursor.execute(SELECT_COUNT_COLLEGES, (COLLEGE_CODE,))
        exists = cursor.fetchone()[0] > 0
        cursor.close()

        if exists:
            flash("Error: College code already exists!", category="error")
            return redirect(url_for('colleges.collegesPage'))

        # Insert new college
        cursor = mysql.connection.cursor()
        cursor.execute(
            INSERT_INTO_COLLEGE,
            (COLLEGE_CODE, COLLEGE_NAME)
        )
        mysql.connection.commit()
        cursor.close()

        flash("College added successfully", category="success")
        return redirect(url_for('colleges.collegesPage'))

    # Get current page from query string
    current_page = request.args.get('page', 1, type=int)
    offset = (current_page - 1) * PER_PAGE

    # Get total colleges count
    cursor = mysql.connection.cursor()
    cursor.execute(COUNT_COLLEGE)
    total_colleges = cursor.fetchone()[0]
    cursor.close()



    # Calculate total pages
    total_pages = max(1, (total_colleges + PER_PAGE - 1) // PER_PAGE)


    # Ensure page is within range
    if current_page < 1:
        flash("Invalid page number.", "error")
        return redirect(url_for('colleges.collegesPage', page=1))
    if current_page > total_pages:
        flash("Page out of range.", "error")
        return redirect(url_for('colleges.collegesPage', page=total_pages))

    # Fetch paginated colleges
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        COLLEGE_QUERY_FOUR,
        (PER_PAGE, offset)
    )
    colleges_list = cursor.fetchall()
    cursor.close()

    return render_template(
        "colleges.html",
        colleges=colleges_list,
        current_page=current_page,
        total_pages=total_pages
    )
