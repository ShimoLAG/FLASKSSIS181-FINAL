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

SELECT_COURSE = 'SELECT COURSE_CODE, COURSE_NAME, COLLEGE_CODE FROM courses LIMIT %s OFFSET %s'
SELECT_COLLEGE_CODE = 'SELECT COLLEGE_CODE, COLLEGE_NAME FROM colleges'
SELECT_COURSES_COUNT = "SELECT COUNT(*) FROM courses WHERE COURSE_CODE = %s"
INSERT_COURSES_QUERY = "INSERT INTO courses (COURSE_CODE, COURSE_NAME, COLLEGE_CODE) VALUES (%s, %s, %s)"
ANOTHER_COURSE_COUNT = 'SELECT COUNT(*) AS total FROM courses'

def Get_Courses(offset, limit):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(SELECT_COURSE, (limit, offset),)
        courses = cursor.fetchall()
        cursor.close()
        return courses

def GetColleges():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(SELECT_COLLEGE_CODE)
        colleges = cursor.fetchall()
        cursor.close()
        return colleges

def TOTAL():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(ANOTHER_COURSE_COUNT)
        total_courses = cursor.fetchone()['total']
        cursor.close()
        return total_courses

def BELOWTOTAL(COURSE_CODE):
        cursor = mysql.connection.cursor()
        cursor.execute(SELECT_COURSES_COUNT, (COURSE_CODE,))
        exists = cursor.fetchone()[0] > 0
        cursor.close()
        return exists

def INSERTCOURSE(COURSE_CODE, COURSE_NAME, COLLEGE_CODE):
        cursor = mysql.connection.cursor()
        cursor.execute(INSERT_COURSES_QUERY, 
                       (COURSE_CODE, COURSE_NAME, COLLEGE_CODE))
        mysql.connection.commit()
        cursor.close()
       