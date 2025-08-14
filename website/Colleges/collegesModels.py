# queries.py
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
# Queries for students
GET_COURSES = "SELECT COURSE_CODE, COURSE_NAME FROM courses"

SEARCH_STUDENTS_NONE = """
    SELECT students.ID, students.IMAGE, students.FIRST_NAME, students.LAST_NAME,
           students.COURSE_CODE, courses.COURSE_NAME, students.YEAR, students.GENDER
    FROM students
    LEFT JOIN courses ON students.COURSE_CODE = courses.COURSE_CODE
    WHERE students.COURSE_CODE IS NULL
    LIMIT %s OFFSET %s
"""
COUNT_STUDENTS_NONE = """
    SELECT COUNT(*) AS total
    FROM students
    LEFT JOIN courses ON students.COURSE_CODE = courses.COURSE_CODE
    WHERE students.COURSE_CODE IS NULL
"""

SEARCH_COURSE_CODE = """
    SELECT students.ID, students.IMAGE, students.FIRST_NAME, students.LAST_NAME,
           students.COURSE_CODE, courses.COURSE_NAME, students.YEAR, students.GENDER
    FROM students
    LEFT JOIN courses ON students.COURSE_CODE = courses.COURSE_CODE
    WHERE students.COURSE_CODE LIKE %s OR courses.COURSE_NAME LIKE %s
    LIMIT %s OFFSET %s
"""
COUNT_COURSE_CODE = """
    SELECT COUNT(*) AS total
    FROM students
    LEFT JOIN courses ON students.COURSE_CODE = courses.COURSE_CODE
    WHERE students.COURSE_CODE LIKE %s OR courses.COURSE_NAME LIKE %s
"""

DELETE_STUDENT = "DELETE FROM students WHERE ID = %s"
DELETE_COURSE = "DELETE FROM courses WHERE COURSE_CODE = %s"
DELETE_COLLEGE = "DELETE FROM colleges WHERE COLLEGE_CODE = %s"

UPDATE_COLLEGE = """
    UPDATE colleges
    SET COLLEGE_CODE = %s, COLLEGE_NAME = %s
    WHERE COLLEGE_CODE = %s
"""

UPDATE_COURSE = """
    UPDATE courses
    SET COURSE_CODE = %s, COURSE_NAME = %s, COLLEGE_CODE = %s
    WHERE COURSE_CODE = %s
"""

UPDATE_STUDENT = """
    UPDATE students
    SET ID = %s, IMAGE = %s, FIRST_NAME = %s, LAST_NAME = %s, COURSE_CODE = %s, YEAR = %s, GENDER = %s
    WHERE ID = %s
"""


def search_students_by_field(search_field):
    return f"""
        SELECT students.ID, students.IMAGE, students.FIRST_NAME, students.LAST_NAME,
               students.COURSE_CODE, courses.COURSE_NAME, students.YEAR, students.GENDER
        FROM students
        LEFT JOIN courses ON students.COURSE_CODE = courses.COURSE_CODE
        WHERE students.{search_field} LIKE %s
        LIMIT %s OFFSET %s
    """

SELECT_COUNT_COLLEGES = "SELECT COUNT(*) FROM colleges WHERE COLLEGE_CODE = %s"
INSERT_INTO_COLLEGE = "INSERT INTO colleges (COLLEGE_CODE, COLLEGE_NAME) VALUES (%s, %s)"
COUNT_COLLEGE = "SELECT COUNT(*) FROM colleges"
COLLEGE_QUERY_FOUR = "SELECT COLLEGE_CODE, COLLEGE_NAME FROM colleges ORDER BY COLLEGE_CODE ASC LIMIT %s OFFSET %s"

def CHECK_IF_EXISTS(COLLEGE_CODE):
    cursor = mysql.connection.cursor()
    cursor.execute(SELECT_COUNT_COLLEGES, (COLLEGE_CODE,))
    exists = cursor.fetchone()[0] > 0
    cursor.close()
    
    if exists:
            return exists

def COUNT_COLLEGES(COLLEGE_CODE, COLLEGE_NAME):
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

def COLLEGE_COUNT():
    cursor = mysql.connection.cursor()
    cursor.execute(COUNT_COLLEGE)
    total_colleges = cursor.fetchone()[0]
    cursor.close()
    return total_colleges

def PAGES_COLLEGES(PER_PAGE, offset):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
        COLLEGE_QUERY_FOUR,
        (PER_PAGE, offset)
    )
        colleges_list = cursor.fetchall()
        cursor.close()

        return colleges_list
