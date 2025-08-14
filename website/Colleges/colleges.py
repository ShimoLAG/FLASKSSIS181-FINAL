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
from .collegesModels import (SELECT_COUNT_COLLEGES, INSERT_INTO_COLLEGE, COUNT_COLLEGE, COLLEGE_QUERY_FOUR, CHECK_IF_EXISTS, COUNT_COLLEGES, COLLEGE_COUNT, PAGES_COLLEGES)


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


        exists = CHECK_IF_EXISTS(COLLEGE_CODE)
        if exists:
            flash("Error: College code already exists!", category="error")
            return redirect(url_for('colleges.collegesPage'))

        
        COUNT_COLLEGES(COLLEGE_CODE, COLLEGE_NAME)

    # Get current page from query string
    current_page = request.args.get('page', 1, type=int)
    offset = (current_page - 1) * PER_PAGE

    # Get total colleges count
    total_colleges = COLLEGE_COUNT()



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
    colleges_list = PAGES_COLLEGES(PER_PAGE, offset)

    return render_template(
        "colleges.html",
        colleges=colleges_list,
        current_page=current_page,
        total_pages=total_pages
    )
