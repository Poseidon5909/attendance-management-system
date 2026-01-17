from flask import Blueprint

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return "Attendance Management System is running 🚀"
