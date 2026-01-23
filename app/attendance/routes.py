from flask import render_template, request, redirect, url_for, flash, session
from datetime import date

from app.attendance import attendance
from app.models import Student, Attendance
from app.extensions import db
from sqlalchemy import func, case


def login_required():
    return "user_id" in session

@attendance.route("/student-report")
def student_report():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    report = db.session.query(
        Student.name,
        func.sum(case((Attendance.status == "Present", 1), else_=0)).label("present"),
        func.sum(case((Attendance.status == "Absent", 1), else_=0)).label("absent")
    ).join(Attendance).group_by(Student.id).all()

    return render_template("student_report.html", report=report)

@attendance.route("/mark", methods=["GET", "POST"])
def mark_attendance():
    if not login_required():
        return redirect(url_for("auth.login"))

    students = Student.query.order_by(Student.roll_number).all()

    if request.method == "POST":
        selected_date = request.form.get("date")

        if not selected_date:
            flash("Please select a date", "danger")
            return redirect(url_for("attendance.mark_attendance"))

        for student in students:
            status = request.form.get(f"status_{student.id}")

            exists = Attendance.query.filter_by(
                student_id=student.id,
                date=selected_date
            ).first()

            if exists:
                continue

            record = Attendance(
                student_id=student.id,
                date=selected_date,
                status=status
            )
            db.session.add(record)

        db.session.commit()
        flash("Attendance marked successfully", "success")
        return redirect(url_for("attendance.view_attendance", date=selected_date))

    return render_template("mark_attendance.html", students=students)


@attendance.route("/view", methods=["GET"])
def view_attendance():
    if not login_required():
        return redirect(url_for("auth.login"))

    selected_date = request.args.get("date")
    records = []

    if selected_date:
        records = Attendance.query.filter_by(date=selected_date).all()

    return render_template(
        "view_attendance.html",
        records=records,
        selected_date=selected_date
    )

@attendance.route("/date-report", methods=["GET"])
def date_report():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    start = request.args.get("start")
    end = request.args.get("end")
    records = []

    if start and end:
        records = Attendance.query.filter(
            Attendance.date.between(start, end)
        ).all()

    return render_template(
        "date_report.html",
        records=records,
        start=start,
        end=end
    )
