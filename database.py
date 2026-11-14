
import sqlite3


def create_table():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            roll_no TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            course TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            roll_no TEXT PRIMARY KEY,
            mathematics INTEGER,
            python INTEGER,
            statistics INTEGER,
            total INTEGER,
            percentage REAL,
            grade TEXT
       )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            roll_no TEXT PRIMARY KEY,
            total_classes INTEGER,
            present INTEGER,
            absent INTEGER,
            percentage REAL
       )
   """)
    conn.commit()
    conn.close()


def insert_student(roll_no, name, age, course):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students (roll_no, name, age, course)
        VALUES (?, ?, ?, ?)
    """, (roll_no, name, age, course))

    conn.commit()
    conn.close()

    print("Student added successfully!")


def view_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()
    return students


# ADD THIS FUNCTION
def search_student(roll_no):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    student = cursor.fetchone()

    conn.close()
    return student

def update_student(roll_no, name, age, course):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET name = ?, age = ?, course = ?
        WHERE roll_no = ?
    """, (name, age, course, roll_no))

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated

def delete_student(roll_no):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    conn.commit()

    deleted = cursor.rowcount

    conn.close()

    return deleted

def save_marks(roll_no, mathematics, python, statistics,
               total, percentage, grade):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO marks
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (roll_no, mathematics, python, statistics,
          total, percentage, grade))

    conn.commit()
    conn.close()

    print("Marks saved successfully!")

def get_all_results():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT students.roll_no,
               students.name,
               marks.total,
               marks.percentage,
               marks.grade
        FROM students
        INNER JOIN marks
        ON students.roll_no = marks.roll_no
        ORDER BY marks.percentage DESC
    """)

    results = cursor.fetchall()

    conn.close()

    return results

def get_student_report(roll_no):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT students.roll_no,
               students.name,
               students.age,
               students.course,
               marks.mathematics,
               marks.python,
               marks.statistics,
               marks.total,
               marks.percentage,
               marks.grade
        FROM students
        LEFT JOIN marks
        ON students.roll_no = marks.roll_no
        WHERE students.roll_no = ?
    """, (roll_no,))

    report = cursor.fetchone()

    conn.close()

    return report

def save_attendance(roll_no, total_classes, present, absent, percentage):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO attendance
        VALUES (?, ?, ?, ?, ?)
    """, (roll_no, total_classes, present, absent, percentage))

    conn.commit()
    conn.close()

    print("Attendance saved successfully!")


def get_attendance(roll_no):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM attendance
        WHERE roll_no = ?
    """, (roll_no,))

    attendance = cursor.fetchone()

    conn.close()

    return attendance 

def get_dashboard_stats():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    # Total number of students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    # Average percentage
    cursor.execute("SELECT AVG(percentage) FROM marks")
    average_percentage = cursor.fetchone()[0]

    # Overall attendance
    cursor.execute("""
        SELECT SUM(present), SUM(total_classes)
        FROM attendance
    """)
    attendance = cursor.fetchone()

    conn.close()

    average_percentage = round(average_percentage or 0, 2)

    if attendance[1] and attendance[1] > 0:
        attendance_percentage = round(
            (attendance[0] / attendance[1]) * 100, 2
        )
    else:
        attendance_percentage = 0

    return total_students, average_percentage, attendance_percentage

def get_all_attendance():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT students.roll_no,
               students.name,
               attendance.total_classes,
               attendance.present,
               attendance.absent,
               attendance.percentage
        FROM students
        INNER JOIN attendance
        ON students.roll_no = attendance.roll_no
        ORDER BY attendance.percentage DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records

def get_subject_averages():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            AVG(mathematics),
            AVG(python),
            AVG(statistics)
        FROM marks
    """)

    averages = cursor.fetchone()

    conn.close()

    return averages

def get_grade_distribution():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT marks.grade, COUNT(*)
        FROM students
        INNER JOIN marks
        ON students.roll_no = marks.roll_no
        GROUP BY marks.grade
        ORDER BY
            CASE marks.grade
                WHEN 'A+' THEN 1
                WHEN 'A' THEN 2
                WHEN 'B+' THEN 3
                WHEN 'B' THEN 4
                WHEN 'C+' THEN 5
                WHEN 'C' THEN 6
                WHEN 'D' THEN 7
                ELSE 8
            END
  """)

    records = cursor.fetchall()

    conn.close()

    return records

def get_attendance_performance():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            students.roll_no,
            students.name,
            marks.percentage,
            attendance.percentage
        FROM students
        INNER JOIN marks
        ON students.roll_no = marks.roll_no
        INNER JOIN attendance
        ON students.roll_no = attendance.roll_no
        ORDER BY marks.percentage DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records

if __name__ == "__main__":
   
    create_table()