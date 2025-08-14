from flask import Flask
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os

mysql = MySQL()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
   
    app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
    app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
    app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
    app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")

    mysql.init_app(app)

    from .Colleges.colleges import routes as colleges
    from .Colleges.collegesController import controller as collegesController
    from .Students.students import routes as students
    from .Students.studentsController import controller as studentsController
    from .Courses.courses import routes as courses
    from .Courses.coursesController import controller as coursesController

    app.register_blueprint(colleges, url_prefix='/colleges')
    app.register_blueprint(collegesController, url_prefix='/colleges')
    app.register_blueprint(students)
    app.register_blueprint(studentsController, url_prefix='/students')
    app.register_blueprint(courses, url_prefix='/courses')
    app.register_blueprint(coursesController, url_prefix='/courses')

    return app