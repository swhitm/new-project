from __future__ import annotations

import streamlit as st

from enrollment_starter import (
    CURRENT_STUDENT,
    create_tables,
    enroll_with_key,
    get_student_course_record,
    get_student_enrollments,
    seed_sample_data,
    soft_unenroll_student,
)


def init_session_state() -> None:
    defaults = {
        "current_page": "dashboard",
        "selected_class": None,
        "role": "student",
        "feedback_messages": [],
        "enrollment_key": "",
    }

    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def add_feedback(message: str, message_type: str = "success") -> None:
    st.session_state.feedback_messages.append(
        {"type": message_type, "message": message}
    )


def display_feedback_messages() -> None:
    if not st.session_state.feedback_messages:
        return

    for feedback in st.session_state.feedback_messages:
        message = feedback.get("message", "")
        message_type = feedback.get("type", "info")

        if message_type == "success":
            st.success(message)
        elif message_type == "error":
            st.error(message)
        elif message_type == "warning":
            st.warning(message)
        else:
            st.info(message)

    st.session_state.feedback_messages = []


def handle_enroll() -> None:
    enrollment_key = st.session_state.enrollment_key.strip()
    if not enrollment_key:
        add_feedback("Please enter an enrollment key before enrolling.", "warning")
        return

    record = enroll_with_key(
        CURRENT_STUDENT["user_id"], CURRENT_STUDENT["email"], enrollment_key
    )

    if record:
        add_feedback(
            f"Successfully enrolled in {record['course_id']} - {record['course_name']}",
            "success",
        )
        st.session_state.enrollment_key = ""
    else:
        add_feedback(
            "Enrollment failed. Please check the enrollment key and try again.",
            "error",
        )


def handle_view_class(course: dict[str, str]) -> None:
    st.session_state.selected_class = course
    st.session_state.current_page = "class_details"


def handle_soft_unenroll(course_id: str) -> None:
    success = soft_unenroll_student(CURRENT_STUDENT["user_id"], course_id)
    if success:
        add_feedback(
            f"Soft-unenrolled from {course_id}. The class remains on record as withdrawn.",
            "success",
        )
    else:
        add_feedback(
            "Unable to unenroll. Please try again or contact support.",
            "error",
        )


def render_dashboard() -> None:
    st.title("Student Dashboard")
    st.write(
        f"Logged in as **{CURRENT_STUDENT['name']}** ({CURRENT_STUDENT['email']})"
    )
    display_feedback_messages()

    enrolled_classes = get_student_enrollments(CURRENT_STUDENT["user_id"])

    with st.container():
        st.subheader("Enrolled Classes")
        if enrolled_classes:
            class_rows = [
                {
                    "Course ID": record["course_id"],
                    "Course Name": record["course_name"],
                    "Instructor": record["instructor"],
                    "Status": record["status"].capitalize(),
                    "Enrolled At": record["enrolled_at"],
                }
                for record in enrolled_classes
            ]
            st.dataframe(class_rows, use_container_width=True)

            st.write("---")
            for record in enrolled_classes:
                row_columns = st.columns([3, 1, 1])
                with row_columns[0]:
                    st.markdown(
                        f"**{record['course_id']} – {record['course_name']}**"
                    )
                    st.write(f"Instructor: {record['instructor']}")
                    st.write(f"Status: {record['status'].capitalize()}")
                with row_columns[1]:
                    if st.button(
                        "View Class",
                        key=f"view_{record['course_id']}",
                    ):
                        handle_view_class(record)
                with row_columns[2]:
                    if st.button(
                        "Soft Unenroll",
                        key=f"unenroll_{record['course_id']}",
                    ):
                        handle_soft_unenroll(record["course_id"])
        else:
            st.warning("No enrolled classes are currently available.")

    with st.container():
        st.subheader("Enroll in a Class")
        enrollment_col, action_col = st.columns([3, 1])
        with enrollment_col:
            st.text_input(
                "Enrollment Key",
                key="enrollment_key",
                placeholder="Enter a course enrollment key",
            )
        with action_col:
            if st.button("Enroll/Re-enroll"):
                handle_enroll()


def render_class_details() -> None:
    st.title("Class Details")
    display_feedback_messages()

    selected_class = st.session_state.selected_class
    if not selected_class:
        st.error("No class selected. Returning to the dashboard.")
        st.session_state.current_page = "dashboard"
        return

    with st.container():
        st.subheader("Selected Class Information")
        info_columns = st.columns([2, 2])
        with info_columns[0]:
            st.write(f"**Course ID:** {selected_class['course_id']}")
            st.write(f"**Course Name:** {selected_class['course_name']}")
            st.write(f"**Instructor:** {selected_class['instructor']}")
        with info_columns[1]:
            st.write(
                f"**Enrollment Status:** {selected_class['status'].capitalize()}"
            )
            st.write(f"**Enrolled At:** {selected_class['enrolled_at']}")

        st.write("---")
        st.subheader("Course Details")
        st.write(
            "This view displays seeded course metadata for the selected enrollment."
        )
        st.write(
            "Use the dashboard to enroll, re-enroll, or soft-unenroll from classes."
        )

    if st.button("Return to Dashboard"):
        st.session_state.current_page = "dashboard"
        st.session_state.selected_class = None
        add_feedback("Returned to the dashboard.", "success")


def main() -> None:
    create_tables()
    seed_sample_data()
    init_session_state()

    if st.session_state.current_page == "class_details":
        render_class_details()
    else:
        render_dashboard()


if __name__ == "__main__":
    main()
