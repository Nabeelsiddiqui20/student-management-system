

from database import (
    insert_student, 
    view_students,
    search_student,
    update_student,
    delete_student,
    save_marks,
    get_all_results,
    get_student_report,
    save_attendance,
    get_attendance,
    create_table
)
create_table()

students = []

# Function to register a student
def register_student():

    print("\n===== REGISTER STUDENT =====")

    roll_no = input("Enter Roll Number: ")
    name = input("Enter Student Name: ")
    age = int(input("Enter Age: "))
    course = input("Enter Course: ")

    try:
        insert_student(roll_no, name, age, course)
    except Exception as e:
        print("Error:", e)


# Function to display all students
def display_students():

    print("\n===== ALL REGISTERED STUDENTS =====")

    students = view_students()

    if not students:
        print("No students registered yet.")
    else:
        for student in students:
            print(student)


def search_student_menu():

    print("\n===== SEARCH STUDENT =====")

    roll_no = input("Enter Roll Number: ")

    student = search_student(roll_no)

    if student:
        print("\nStudent Found!")
        print("Roll Number:", student[0])
        print("Name:", student[1])
        print("Age:", student[2])
        print("Course:", student[3])

    else:
        print("Student not found!")

def update_student_menu():

    print("\n===== UPDATE STUDENT =====")

    roll_no = input("Enter Roll Number: ")

    student = search_student(roll_no)

    if student:

        print("Student Found!")

        name = input("Enter New Name: ")
        age = int(input("Enter New Age: "))
        course = input("Enter New Course: ")

        result = update_student(roll_no, name, age, course)

        if result:
            print("Student updated successfully!")
        else:
            print("Update failed!")

    else:
        print("Student not found!")

def delete_student_menu():

    print("\n===== DELETE STUDENT =====")

    roll_no = input("Enter Roll Number: ")

    student = search_student(roll_no)

    if student:

        print("Student Found!")
        print("Name:", student[1])

        confirm = input("Are you sure you want to delete? (yes/no): ")

        if confirm.lower() == "yes":

            result = delete_student(roll_no)

            if result:
                print("Student deleted successfully!")

        else:
            print("Deletion cancelled!")

    else:
        print("Student not found!")

def add_marks():

    roll_no = input("\nEnter Student Roll Number: ")

    # Search student in SQLite database
    student = search_student(roll_no)

    if student:

        print("\nStudent Found:", student[1])
        print("\nEnter Subject Marks")

        maths = int(input("Mathematics (out of 100): "))
        python = int(input("Python Programming (out of 100): "))
        statistics = int(input("Statistics (out of 100): "))

        # Validate marks
        if not all(0 <= mark <= 100 for mark in [maths, python, statistics]):
            print("Invalid marks! Enter marks between 0 and 100.")
            return

        # Calculate total and percentage
        total = maths + python + statistics
        percentage = (total / 300) * 100

        # Calculate grade
        if percentage >= 90:
            grade = "A+"
        elif percentage >= 80:
            grade = "A"
        elif percentage >= 70:
            grade = "B"
        elif percentage >= 60:
            grade = "C"
        elif percentage >= 40:
            grade = "D"
        else:
            grade = "F"

        # Save marks permanently in SQLite
        save_marks(
            roll_no, maths, python, statistics,
            total, percentage, grade
        )

        # Display result
        print("\n===== STUDENT RESULT =====")
        print("Name:", student[1])
        print("Mathematics:", maths)
        print("Python:", python)
        print("Statistics:", statistics)
        print("Total:", total, "/ 300")
        print("Percentage:", round(percentage, 2), "%")
        print("Grade:", grade)

    else:
        print("Student not found!")

def student_ranking():

    print("\n===== STUDENT PERFORMANCE RANKING =====")

    results = get_all_results()

    if not results:
        print("No student marks available yet.")
        return

    for rank, student in enumerate(results, start=1):

        print("\nRank:", rank)
        print("Roll Number:", student[0])
        print("Name:", student[1])
        print("Total Marks:", student[2], "/ 300")
        print("Percentage:", round(student[3], 2), "%")
        print("Grade:", student[4])

        print("------------------------------")

def attendance_management():

    roll_no = input("\nEnter Student Roll Number: ")

    # Search student in SQLite
    student = search_student(roll_no)

    if student:

        print("\nStudent Found:", student[1])

        total_classes = int(input("Enter Total Classes: "))
        present_classes = int(input("Enter Classes Attended: "))

        if total_classes <= 0:
            print("Total classes must be greater than zero!")
            return

        if present_classes < 0 or present_classes > total_classes:
            print("Invalid attendance details!")
            return

        # Calculate attendance
        absent = total_classes - present_classes

        attendance_percentage = (
            present_classes / total_classes
        ) * 100

        attendance_percentage = round(attendance_percentage, 2)

        # Save attendance in SQLite
        save_attendance(
            roll_no,
            total_classes,
            present_classes,
            absent,
            attendance_percentage
        )

        # Display attendance report
        print("\n====== ATTENDANCE REPORT ======")
        print("Name:", student[1])
        print("Roll Number:", roll_no)
        print("Total Classes:", total_classes)
        print("Present:", present_classes)
        print("Absent:", absent)
        print("Attendance:", attendance_percentage, "%")

        if attendance_percentage >= 75:
            print("Status: Eligible")
        else:
            print("Status: Shortage of Attendance")

    else:
        print("Student not found!")

def student_report():

    print("\n===== STUDENT REPORT =====")

    roll_no = input("Enter Student Roll Number: ")

    report = get_student_report(roll_no)

    if report:

        print("\n===== STUDENT DETAILS =====")
        print("Roll Number:", report[0])
        print("Name:", report[1])
        print("Age:", report[2])
        print("Course:", report[3])

        print("\n===== ACADEMIC PERFORMANCE =====")

        if report[4] is not None:

            print("Mathematics:", report[4])
            print("Python:", report[5])
            print("Statistics:", report[6])
            print("Total:", report[7], "/ 300")
            print("Percentage:", round(report[8], 2), "%")
            print("Grade:", report[9])

        else:
            print("Marks have not been entered yet.")

        # ATTENDANCE REPORT
        attendance = get_attendance(roll_no)

        print("\n===== ATTENDANCE REPORT =====")

        if attendance:

            print("Total Classes:", attendance[1])
            print("Present:", attendance[2])
            print("Absent:", attendance[3])
            print("Attendance:", attendance[4], "%")

            if attendance[4] >= 75:
                print("Status: Eligible")
            else:
                print("Status: Shortage of Attendance")

        else:
            print("Attendance has not been entered yet.")

    else:
        print("Student not found!")
# Main menu
while True:

    print("\n================================")
    print("   STUDENT MANAGEMENT SYSTEM")
    print("================================")
    print("1. Register Student")
    print("2. display Students")
    print("3. Search Student Menu")
    print("4. Update Student Menu")
    print("5. Delete Student Menu")
    print("6. Add Marks")
    print("7. Student Performance Ranking")
    print("8. Attendance Management")
    print("9. Student Report")
    print("10. Exit")
    choice = input("\nEnter your choice: ")

    if choice == "1":
        register_student()

    elif choice == "2":
        display_students()

    elif choice == "3":
        search_student_menu()

    elif choice == "4":
        update_student_menu()

    elif choice == "5":
        delete_student_menu()

    elif choice == "6":
        add_marks()

    elif choice == "7":
        student_ranking()

    elif choice == "8":
        attendance_management()

    elif choice == "9":
        student_report()
    
    elif choice == "10":
        print("Thank you for using our application!")
        break
    else:
        print("Invalid choice! Please try again.")
    