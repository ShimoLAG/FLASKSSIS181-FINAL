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

import re
from flask import flash, redirect, url_for, render_template, request
import MySQLdb
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
STUDENTS_PAGE = """
        SELECT students.ID, students.IMAGE, students.FIRST_NAME, students.LAST_NAME,
               students.COURSE_CODE, courses.COURSE_NAME, students.YEAR, students.GENDER
        FROM students
        LEFT JOIN courses ON students.COURSE_CODE = courses.COURSE_CODE
        LIMIT %s OFFSET %s
        """
STUDENT_GET_COURSES = 'SELECT COURSE_CODE, COURSE_NAME FROM courses'
SELECT_COURSES_STUDENTS = 'SELECT COUNT(*) AS total FROM students'
CHECK_ID_STUDENTS = "SELECT COUNT(*) FROM students WHERE ID = %s"

def Get_Students(offset, limit):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(STUDENTS_PAGE, (limit, offset))
        student = cursor.fetchall()
        cursor.close()
        return student

def getCourses():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(STUDENT_GET_COURSES)
        cour = cursor.fetchall()
        cursor.close()
        return cour

def studPages():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(SELECT_COURSES_STUDENTS)
        total_students = cursor.fetchone()['total']
        cursor.close()
        return total_students

def checkID(ID, IMAGE, FIRST_NAME, LAST_NAME, COURSE_CODE, YEAR, GENDER):
        cursor = mysql.connection.cursor()

        # Check if the ID already exists
        cursor.execute(CHECK_ID_STUDENTS, (ID,))
        count = cursor.fetchone()[0]
        id_pattern = r'^\d{4}-\d{4}$'
        if count > 0:
            flash("Error: ID already exists. Please use a different ID.", category="error")
        elif not FIRST_NAME or not LAST_NAME:
            flash("Error: First Name and Last Name cannot be empty.", category="error")
        elif not re.match(id_pattern, ID):
            flash("Error: ID must follow the format 0000-0000.", category="error")
        else:
            # Insert new student if validation passes
            cursor.execute(
                "INSERT INTO students (ID, IMAGE, FIRST_NAME, LAST_NAME, COURSE_CODE, YEAR, GENDER) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (ID, IMAGE, FIRST_NAME, LAST_NAME, COURSE_CODE, YEAR, GENDER)
            )
            mysql.connection.commit()
            flash("Student added successfully!", category="success")
     


        