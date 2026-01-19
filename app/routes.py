from flask import Blueprint, render_template, redirect, url_for, session
from sqlalchemy import func

from app.models import Student, Attendance
from app.extensions import db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return redirect(url_for("auth.login"))

@main.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    total_students = db.session.query(func.count(Student.id)).scalar()

    attendance_days = db.session.query(
        func.count(func.distinct(Attendance.date))
    ).scalar()

    total_records = db.session.query(func.count(Attendance.id)).scalar()

    present_count = db.session.query(func.count(Attendance.id))\
        .filter(Attendance.status == "Present").scalar()

    attendance_percentage = (
        (present_count / total_records) * 100
        if total_records else 0
    )

    return render_template(
        "dashboard.html",
        total_students=total_students,
        attendance_days=attendance_days,
        attendance_percentage=round(attendance_percentage, 2)
    )
