# Attendance Management System

A professional Flask-based web application for managing student attendance with role-based access control, detailed reporting, and a clean Bootstrap interface.

## Features

- **User Authentication**: Secure admin login system with password hashing
- **Student Management**: Add, edit, and delete student records with roll numbers and contact information
- **Attendance Tracking**: Mark attendance for multiple students in bulk with date selection
- **Comprehensive Reports**:
  - Student-wise attendance summaries with attendance percentages
  - Date-range based attendance reports
  - Real-time attendance statistics on the dashboard
- **Clean UI**: Bootstrap 5 responsive design with intuitive navigation
- **Error Handling**: Custom 404 and 500 error pages with professional styling

## Technology Stack

- **Framework**: Flask 3.1.2
- **ORM**: SQLAlchemy 2.0.45 with Flask-SQLAlchemy 3.1.1
- **Database**: PostgreSQL (configurable)
- **Frontend**: Bootstrap 5.3.2, HTML5, Jinja2 templating
- **Backend Utilities**: Werkzeug for security

## Project Structure

```
attendance-management-system/
├── app/
│   ├── __init__.py                 # Flask app factory with error handlers
│   ├── extensions.py               # SQLAlchemy database instance
│   ├── models.py                   # Database models (User, Student, Attendance)
│   ├── routes.py                   # Main blueprint with dashboard and index
│   ├── auth/                       # Authentication blueprint
│   │   ├── __init__.py
│   │   └── routes.py               # Login and logout routes
│   ├── students/                   # Student management blueprint
│   │   ├── __init__.py
│   │   └── routes.py               # CRUD operations for students
│   ├── attendance/                 # Attendance management blueprint
│   │   ├── __init__.py
│   │   └── routes.py               # Mark attendance and generate reports
│   ├── static/                     # Static assets (CSS, JS, images)
│   └── templates/                  # HTML templates
│       ├── base.html               # Base layout with navbar and flash messages
│       ├── login.html              # Admin login page
│       ├── dashboard.html          # Main dashboard with statistics
│       ├── students.html           # Students list view
│       ├── add_student.html        # Add student form
│       ├── edit_student.html       # Edit student form
│       ├── mark_attendance.html    # Mark attendance form
│       ├── view_attendance.html    # View attendance by date
│       ├── student_report.html     # Student attendance report
│       ├── date_report.html        # Date range attendance report
│       └── errors/
│           ├── 404.html            # Not found error page
│           └── 500.html            # Server error page
├── config.py                       # Application configuration
├── run.py                          # Entry point for running the application
├── requirements.txt                # Production dependencies
├── .gitignore                      # Git ignore patterns
└── README.md                       # This file
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database (or SQLite for development)
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd attendance-management-system
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database** (in `config.py`)
   ```python
   SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost:5432/attendance_db"
   # Or for SQLite (development):
   # SQLALCHEMY_DATABASE_URI = "sqlite:///attendance.db"
   ```

5. **Initialize database** (optional, for first-time setup)
   ```bash
   python
   >>> from app import create_app, db
   >>> app = create_app()
   >>> with app.app_context():
   ...     db.create_all()
   ```

6. **Run the application**
   ```bash
   python run.py
   ```
   
   The application will be available at `http://localhost:5000`

## Usage

### Admin Login
1. Navigate to the login page (`/login`)
2. Enter credentials (admin email and password)
3. Access the dashboard and manage students and attendance

### Key Operations

- **Dashboard**: View summary statistics including total students, attendance days, and overall attendance percentage
- **Add Student**: Create new student records with roll number and email
- **Mark Attendance**: Select a date and mark attendance status (Present/Absent) for all students
- **View Attendance**: Check attendance records filtered by specific date
- **Reports**: Generate attendance reports by student or date range

## Routes & Endpoints

| Method | Route | Endpoint | Description |
|--------|-------|----------|-------------|
| GET | `/` | `main.index` | Redirect to login |
| GET | `/dashboard` | `main.dashboard` | Admin dashboard |
| GET, POST | `/login` | `auth.login` | Admin login |
| GET | `/logout` | `auth.logout` | Admin logout |
| GET, POST | `/students/add` | `students.add_student` | Add new student |
| GET | `/students/` | `students.list_students` | View all students |
| GET, POST | `/students/edit/<id>` | `students.edit_student` | Edit student |
| GET | `/students/delete/<id>` | `students.delete_student` | Delete student |
| GET, POST | `/attendance/mark` | `attendance.mark_attendance` | Mark attendance |
| GET | `/attendance/view` | `attendance.view_attendance` | View attendance by date |
| GET | `/attendance/student-report` | `attendance.student_report` | Student attendance report |
| GET | `/attendance/date-report` | `attendance.date_report` | Date range report |

## Database Models

### User
- `id` (Integer, Primary Key)
- `username` (String, Unique)
- `email` (String, Unique)
- `password_hash` (String)
- `created_at` (DateTime)

### Student
- `id` (Integer, Primary Key)
- `roll_number` (String, Unique)
- `name` (String)
- `email` (String, Unique, Optional)
- `created_at` (DateTime)
- `attendance_records` (Relationship)

### Attendance
- `id` (Integer, Primary Key)
- `student_id` (Foreign Key)
- `date` (Date)
- `status` (String: 'Present' or 'Absent')
- `marked_at` (DateTime)

## Configuration

### Environment Variables
Create a `.env` file (not tracked by git) for sensitive configuration:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/attendance_db
FLASK_ENV=production
```

### Application Settings (config.py)
```python
class Config:
    SECRET_KEY = "your-secret-key"
    SQLALCHEMY_DATABASE_URI = "postgresql://..."
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

## Best Practices Implemented

- **Flask Application Factory Pattern**: Clean app initialization in `create_app()`
- **Blueprint Modularization**: Organized routes into `auth`, `students`, `attendance`, and `main` blueprints
- **Single SQLAlchemy Instance**: Centralized database instance in `extensions.py`
- **Error Handlers**: Custom handlers for 404 and 500 errors with user-friendly templates
- **Password Security**: Werkzeug password hashing for secure password storage
- **Template Inheritance**: Base layout for consistent styling and navigation
- **Flash Messages**: User feedback via Bootstrap alerts
- **CSRF Protection**: Built-in Flask form protection
- **Session-based Authentication**: Secure session management for user authentication

## Development

### Running in Debug Mode
```bash
# Set debug to True in run.py or:
export FLASK_ENV=development
export FLASK_DEBUG=1
python run.py
```

### Testing Routes
```bash
python -c "from app import create_app; app = create_app(); [print(rule) for rule in app.url_map.iter_rules()]"
```

## Deployment

### Production Checklist
- [ ] Set `SECRET_KEY` to a strong random value
- [ ] Set `FLASK_ENV=production`
- [ ] Disable debug mode
- [ ] Use a production WSGI server (Gunicorn, uWSGI)
- [ ] Configure PostgreSQL for production
- [ ] Set up HTTPS/SSL
- [ ] Use environment variables for sensitive data
- [ ] Regular database backups

### Deployment Example (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

## Security Considerations

- ✓ Password hashing with Werkzeug
- ✓ Session-based authentication
- ✓ CSRF protection in forms
- ✓ SQL injection prevention (SQLAlchemy ORM)
- ✓ Secure error pages (no sensitive information leaked)
- ✓ Hidden sensitive files (`.env`, `venv/`, `__pycache__/`) via `.gitignore`

## Troubleshooting

### Database Connection Error
- Verify PostgreSQL is running
- Check connection string in `config.py`
- Ensure database user has proper permissions

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Run on different port
python run.py  # Edit run.py and change port number
```

## Contributing

1. Create a feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## License

This project is open-source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on the repository.

---

**Last Updated**: 2026  
**Status**: Production Ready
