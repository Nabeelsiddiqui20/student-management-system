
import streamlit as st
from database import (
    create_table,
    get_dashboard_stats,
    insert_student,
    view_students,
    search_student,
    update_student,
    delete_student,
    save_marks,
    get_all_results,
    get_student_report,
    get_attendance,
    save_attendance,
    get_all_attendance,
    get_subject_averages,
    get_grade_distribution,
    get_attendance_performance
)

create_table()

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Management System")

# Sidebar navigation
st.sidebar.title("Navigation") 

st.sidebar.markdown("---")

st.sidebar.subheader("🎓 Student Management")

st.sidebar.caption(
    "Manage students, academics and attendance."
)

page = st.sidebar.selectbox(
    "Select Page",
    ["Dashboard", "Register Student", "View Students", "Search Student", "Update Student", "Delete Student", "Add Marks","Performance Ranking", "Student Report", "Attendance Management","Attendance Overview","Performance Analytics"]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Smart Student Management System\n\n"
    "Developed using Python, SQLite and Streamlit."
)
# Dashboard page
if page == "Dashboard":

    st.header("🎓 Smart Student Management System")

    st.write(
        "Welcome to the Student Management and Performance "
        "Analytics Dashboard."
    )

    st.caption(
        "Manage student records, academic results, "
        "attendance and performance analytics."
    )

    st.divider()

    total_students, average_percentage, attendance_percentage = get_dashboard_stats()

    st.subheader("📊 Overall Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "👨‍🎓 Total Students",
            total_students
        )

    with col2:
        st.metric(
            "📚 Class Average",
            f"{average_percentage}%"
        )

    with col3:
        st.metric(
            "📅 Overall Attendance",
            f"{attendance_percentage}%"
        )

    st.divider()

    st.subheader("🚀 System Features")

    col1, col2 = st.columns(2)

    with col1:
        st.write("✅ Student Registration and Management")
        st.write("✅ Marks and Grade Management")
        st.write("✅ Performance Ranking")
        st.write("✅ Individual Student Reports")

    with col2:
        st.write("✅ Attendance Management")
        st.write("✅ Attendance Overview")
        st.write("✅ Performance Analytics")
        st.write("✅ Student Performance Insights")
# Registration page
elif page == "Register Student":

    st.header("📝 Register New Student")

    with st.form("student_registration"):

        roll_no = st.text_input("Enter Roll Number")
        name = st.text_input("Enter Student Name")
        age = st.number_input("Enter Age", min_value=1, max_value=100, step=1)
        course = st.text_input("Enter Course")

        submit = st.form_submit_button("Register Student")

        if submit:

            if not roll_no or not name or not course:
                st.warning("Please fill all the fields.")

            else:
                try:
                    insert_student(roll_no, name, age, course)
                    st.success("Student registered successfully!")

                except Exception as e:
                    st.error(f"Registration failed: {e}")

elif page == "View Students":

    st.header("📋 All Registered Students")

    students = view_students()

    if students:

        st.success(f"Total Students: {len(students)}")

        # Display column headings
        col1, col2, col3, col4 = st.columns(4)

        col1.write("**Roll Number**")
        col2.write("**Name**")
        col3.write("**Age**")
        col4.write("**Course**")

        st.divider()

        # Display each student
        for student in students:

            col1, col2, col3, col4 = st.columns(4)

            col1.write(student[0])
            col2.write(student[1])
            col3.write(student[2])
            col4.write(student[3])

            st.divider()

    else:
        st.info("No students registered yet.")


elif page == "Search Student":

    st.header("🔍 Search Student")

    roll_no = st.text_input("Enter Student Roll Number")

    if st.button("Search Student"):

        if roll_no:

            student = search_student(roll_no)

            if student:

                st.success("Student Found!")

                st.write("### Student Details")

                st.write("**Roll Number:**", student[0])
                st.write("**Name:**", student[1])
                st.write("**Age:**", student[2])
                st.write("**Course:**", student[3])

            else:
                st.error("Student not found!")

        else:
            st.warning("Please enter a roll number.")


elif page == "Update Student":

    st.header("✏️ Update Student Details")

    roll_no = st.text_input("Enter Roll Number")

    if st.button("Find Student"):

        if roll_no:

            student = search_student(roll_no)

            if student:

                st.session_state["student_to_update"] = student
                st.success("Student Found!")

            else:
                st.error("Student not found!")

        else:
            st.warning("Please enter a roll number.")

    if "student_to_update" in st.session_state:

        student = st.session_state["student_to_update"]

        with st.form("update_form"):

            name = st.text_input("Name", value=student[1])
            age = st.number_input(
                "Age",
                min_value=1,
                max_value=100,
                value=student[2]
            )
            course = st.text_input("Course", value=student[3])

            submit = st.form_submit_button("Update Student")

            if submit:

                result = update_student(
                    student[0], name, age, course
                )

                if result:
                    st.success("Student updated successfully!")
                    del st.session_state["student_to_update"]
                else:
                    st.error("Unable to update student.")


elif page == "Delete Student":

    st.header("🗑️ Delete Student")

    roll_no = st.text_input("Enter Student Roll Number")

    if st.button("Find Student"):

        if roll_no:

            student = search_student(roll_no)

            if student:
                st.session_state["student_to_delete"] = student
            else:
                st.error("Student not found!")

        else:
            st.warning("Please enter a roll number.")

    if "student_to_delete" in st.session_state:

        student = st.session_state["student_to_delete"]

        st.warning(
            f"Are you sure you want to delete {student[1]}?"
        )

        if st.button("Confirm Delete", type="primary"):

            result = delete_student(student[0])

            if result:
                st.success("Student deleted successfully!")
                del st.session_state["student_to_delete"]
            else:
                st.error("Unable to delete student.")



elif page == "Add Marks":

    st.header("📝 Add Student Marks")

    with st.form("marks_form"):

        roll_no = st.text_input("Enter Student Roll Number")

        maths = st.number_input(
            "Mathematics Marks",
            min_value=0,
            max_value=100,
            value=0
        )

        python_marks = st.number_input(
            "Python Marks",
            min_value=0,
            max_value=100,
            value=0
        )

        statistics = st.number_input(
            "Statistics Marks",
            min_value=0,
            max_value=100,
            value=0
        )

        submit = st.form_submit_button("Save Marks")

        if submit:
            st.success("FORM SUBMITTED!")

    # This condition must be OUTSIDE the form block
    if submit:

        if not roll_no:
            st.warning("Please enter a roll number.")

        else:
            student = search_student(roll_no.strip())

            if student:

                total = maths + python_marks + statistics

                percentage = round((total / 300) * 100, 2)

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

                save_marks(
                    roll_no.strip(),
                    maths,
                    python_marks,
                    statistics,
                    total,
                    percentage,
                    grade
                )

                st.success(
                    f"Marks saved successfully for {student[1]}!"
                )

                st.subheader("Academic Result")

                st.write("Total Marks:", total, "/ 300")
                st.write("Percentage:", percentage, "%")
                st.write("Grade:", grade)

            else:
                st.error("Student not found!")


elif page == "Performance Ranking":

    st.header("🏆 Student Performance Ranking")

    results = get_all_results()

    if results:

        st.subheader("Class Topper")

        topper = results[0]

        st.success(
            f"🥇 {topper[1]} is the Class Topper "
            f"with {topper[3]}%"
        )

        st.divider()

        st.subheader("Complete Student Rankings")

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.write("**Rank**")
        col2.write("**Roll Number**")
        col3.write("**Name**")
        col4.write("**Percentage**")
        col5.write("**Grade**")

        st.divider()

        for rank, student in enumerate(results, start=1):

            col1, col2, col3, col4, col5 = st.columns(5)

            col1.write(rank)
            col2.write(student[0])
            col3.write(student[1])
            col4.write(f"{student[3]}%")
            col5.write(student[4])

            st.divider()

    else:
        st.info("No student results available yet.")

elif page == "Student Report":

    st.header("📄 Student Academic Report")

    roll_no = st.text_input("Enter Student Roll Number")

    if st.button("Generate Report"):

        if roll_no:

            report = get_student_report(roll_no.strip())

            if report:

                st.success("Student Found!")

                st.subheader("Student Details")

                st.write("Roll Number:", report[0])
                st.write("Name:", report[1])
                st.write("Age:", report[2])
                st.write("Course:", report[3])

                st.divider()

                st.subheader("Academic Performance")

                if report[4] is not None:

                    st.write("Mathematics:", report[4])
                    st.write("Python:", report[5])
                    st.write("Statistics:", report[6])
                    st.write("Total Marks:", report[7], "/ 300")
                    st.write("Percentage:", report[8], "%")
                    st.write("Grade:", report[9])

                else:
                    st.info("Marks have not been added yet.")

                st.divider()

                st.subheader("📅 Attendance Details")

                attendance = get_attendance(roll_no.strip())

                if attendance:

                    st.write("Total Classes:", attendance[1])
                    st.write("Present Classes:", attendance[2])
                    st.write("Absent Classes:", attendance[3])
                    st.write("Attendance Percentage:", attendance[4], "%")

                    if attendance[4] >= 75:
                        st.success("Good Attendance!")
                    else:
                        st.warning("Attendance is below 75%.")

                else:
                    st.info("Attendance has not been recorded yet.")

            else:
                st.error("Student not found!")

        else:
            st.warning("Please enter a roll number.")

elif page == "Attendance Management":

    st.header("📅 Attendance Management")

    with st.form("attendance_form"):

        roll_no = st.text_input("Enter Student Roll Number")

        total_classes = st.number_input(
            "Total Classes",
            min_value=1,
            step=1
        )

        present_classes = st.number_input(
            "Present Classes",
            min_value=0,
            step=1
        )

        submit = st.form_submit_button("Save Attendance")

        if submit:

            if not roll_no:
                st.warning("Please enter a roll number.")

            else:

                student = search_student(roll_no.strip())

                if student:

                    if present_classes > total_classes:

                        st.error(
                            "Present classes cannot exceed total classes!"
                        )

                    else:

                        absent_classes = total_classes - present_classes

                        percentage = round(
                            (present_classes / total_classes) * 100, 2
                        )

                        save_attendance(
                            roll_no.strip(),
                            total_classes,
                            present_classes,
                            absent_classes,
                            percentage
                        )

                        st.success(
                            f"Attendance saved for {student[1]}!"
                        )

                        st.subheader("Attendance Summary")

                        st.write("Total Classes:", total_classes)
                        st.write("Present Classes:", present_classes)
                        st.write("Absent Classes:", absent_classes)
                        st.write("Attendance Percentage:", percentage, "%")

                else:
                    st.error("Student not found!")

elif page == "Attendance Overview":

    st.header("📊 Attendance Overview")

    records = get_all_attendance()

    if records:

        total_students = len(records)

        average_attendance = round(
            sum(student[5] for student in records) / total_students, 2
        )

        low_attendance = [
            student for student in records
            if student[5] < 75
        ]

        col1, col2, col3 = st.columns(3)

        col1.metric("Students with Records", total_students)

        col2.metric(
            "Average Attendance",
            f"{average_attendance}%"
        )

        col3.metric(
            "Below 75% Attendance",
            len(low_attendance)
        )

        st.divider()

        st.subheader("All Student Attendance")

        col1, col2, col3, col4 = st.columns(4)

        col1.write("**Roll Number**")
        col2.write("**Name**")
        col3.write("**Present / Total**")
        col4.write("**Attendance**")

        st.divider()

        for student in records:

            col1, col2, col3, col4 = st.columns(4)

            col1.write(student[0])
            col2.write(student[1])
            col3.write(f"{student[3]} / {student[2]}")
            col4.write(f"{student[5]}%")

            st.divider()

        st.subheader("⚠️ Students Below 75% Attendance")

        if low_attendance:

            for student in low_attendance:

                st.warning(
                    f"{student[1]} ({student[0]}) - "
                    f"{student[5]}% attendance"
                )

        else:

            st.success("All students have attendance above 75%!")

    else:

        st.info("No attendance records available yet.")

elif page == "Performance Analytics":

    st.header("📊 Performance Analytics Dashboard")

    averages = get_subject_averages()

    if averages and averages[0] is not None:

        math_avg = round(averages[0], 2)
        python_avg = round(averages[1], 2)
        statistics_avg = round(averages[2], 2)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Mathematics Average", math_avg)

        with col2:
            st.metric("Python Average", python_avg)

        with col3:
            st.metric("Statistics Average", statistics_avg)

        st.subheader("Subject-wise Average Comparison")

        st.write("Mathematics")
        st.progress(int(math_avg))

        st.write("Python")
        st.progress(int(python_avg))

        st.write("Statistics")
        st.progress(int(statistics_avg))

        st.subheader("🎓 Grade Distribution")

        grade_records = get_grade_distribution()

        if grade_records:

            for grade, count in grade_records:

                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"Grade {grade}")

                with col2:
                    st.write(f"Number of Students: {count}")

        else:
            st.info("No grade records available.")

        st.subheader("📈 Attendance vs Academic Performance")

        records = get_attendance_performance()

        if records:

            for student in records:

                st.write(f"**{student[1]} ({student[0]})**")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Academic Percentage",
                        f"{student[2]}%"
                    )

                with col2:
                    st.metric(
                        "Attendance Percentage",
                        f"{student[3]}%"
                    )

                st.divider()

        else:
            st.info("No matching marks and attendance records found.")
        
        st.info("No marks available to calculate averages.")        

        st.subheader("🏆 Student Performance Insights")

        results = get_all_results()

        if results:

            topper = results[0]
            lowest = results[-1]

            class_average = round(
                sum(student[3] for student in results) / len(results), 2
            )

            above_75 = sum(
                1 for student in results if student[3] >= 75
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "🏆 Topper",
                    topper[1],
                    f"{topper[3]}%"
                )

                st.metric(
                    "📊 Class Average",
                    f"{class_average}%"
                )

            with col2:
                st.metric(
                    "📉 Lowest Performer",
                    lowest[1],
                    f"{lowest[3]}%"
                )

                st.metric(
                    "🌟 Students Above 75%",
                    above_75
                )

        else:
            st.info("No student performance records available.") 

        st.subheader("🔍 Individual Student Performance")

        search_roll = st.text_input(
            "Enter Student Roll Number",
            key="analytics_search"
        )

        if st.button("Search Student Performance"):

            if search_roll.strip():

                student_report = get_student_report(search_roll.strip())

                if student_report:

                    st.success("Student Found!")

                    st.write("Name:", student_report[1])
                    st.write("Roll Number:", student_report[0])
                    st.write("Course:", student_report[3])

                    st.subheader("Subject-wise Marks")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Mathematics", student_report[4])

                    with col2:
                        st.metric("Python", student_report[5])

                    with col3:
                        st.metric("Statistics", student_report[6])

                    st.metric(
                        "Academic Percentage",
                        f"{student_report[8]}%"
                    )

                    st.metric("Grade", student_report[9])

                    attendance = get_attendance(search_roll.strip())

                    if attendance:

                        st.subheader("Attendance Details")

                        st.write("Total Classes:", attendance[1])
                        st.write("Present:", attendance[2])
                        st.write("Absent:", attendance[3])

                        st.metric(
                            "Attendance Percentage",
                            f"{attendance[4]}%"
                        )

                    else:
                        st.info("Attendance record not available.")

                else:
                    st.error("Student not found.")

            else:
                st.warning("Please enter a roll number.")