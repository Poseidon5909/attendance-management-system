from flask import render_template, redirect, url_for, request, flash, session
from app.students import students
from app.models import Student
from app.extensions import db


def login_required():
  return "user_id" in session

@students.route("/add", methods=["GET", "POST"])
def add_student():
    if not login_required():
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        roll = request.form.get("roll_number")
        name = request.form.get("name")
        email = request.form.get("email")

        if not roll or not name:
            flash("Roll number and name are required", "danger")
            return redirect(url_for("students.add_student"))

        existing = Student.query.filter_by(roll_number=roll).first()
        if existing:
            flash("Roll number already exists", "danger")
            return redirect(url_for("students.add_student"))

        student = Student(
            roll_number=roll,
            name=name,
            email=email
        )
        db.session.add(student)
        db.session.commit()

        flash("Student added successfully", "success")
        return redirect(url_for("students.list_students"))

    return render_template("add_student.html")

@students.route("/")
def list_students():
    if not login_required():
        return redirect(url_for("auth.login"))

    students_list = Student.query.all()
    return render_template("students.html", students=students_list)

@students.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    if not login_required():
        return redirect(url_for("auth.login"))

    student = Student.query.get_or_404(id)

    if request.method == "POST":
        student.name = request.form.get("name")
        student.email = request.form.get("email")
        db.session.commit()

        flash("Student updated successfully", "success")
        return redirect(url_for("students.list_students"))

    return render_template("edit_student.html", student=student)

@students.route("/delete/<int:id>")
def delete_student(id):
    if not login_required():
        return redirect(url_for("auth.login"))

    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()

    flash("Student deleted successfully", "success")
    return redirect(url_for("students.list_students"))
