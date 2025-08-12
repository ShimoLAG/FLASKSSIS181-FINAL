from flask import Flask
from flask_mysqldb import MySQL
import MySQLdb.cursors

mysql = MySQL()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thisisarandomsecretkey1111' #encrypts the cookies and session data related to website (dont worry bout it)
    
   
    app.config['MYSQL_HOST'] = "localhost"
    app.config['MYSQL_USER'] = "root"
    app.config['MYSQL_PASSWORD'] = ""
    app.config['MYSQL_DB'] = "fssis"

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