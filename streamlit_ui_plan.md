# Streamlit UI Plan for Student Enrollment Manager

## Overview
This plan outlines a Streamlit-based user interface for the Student Enrollment Manager application. The UI assumes the user is already logged in as the seeded student from the backend. It leverages the existing backend structure and service methods without introducing new authentication systems.

The application follows a two-page student flow:
- **Page 1: Student Dashboard** - Overview of enrolled classes, enrollment actions, and navigation.
- **Page 2: Class Details** - Detailed view of a selected class with enrollment status and return navigation.

## Session State Management
Use `st.session_state` to track the following:
- `current_page`: Tracks the active page ("dashboard" or "class_details").
- `selected_class`: Stores the ID or details of the currently selected class for Page 2.
- `role`: Set to "student" (assumed from login).
- `feedback_messages`: A list or dictionary to store success, error, and warning messages for display.

### Session State Behavior
- Initialize `current_page` to "dashboard" on app start.
- Update `selected_class` when navigating to class details.
- Clear `feedback_messages` after display or on page changes.
- Persist state across reruns for seamless navigation.

## Page 1: Student Dashboard
This page serves as the main hub for student interactions.

### Layout and Elements
- **st.title**: "Student Dashboard"
- **st.container**: Wrap the main content for organization.
- **st.columns**: Use columns to separate enrolled classes list and enrollment actions.
- **st.dataframe**: Display enrolled classes in a table format (columns: Class ID, Course Name, Enrollment Status).
- **st.text_input**: Input field for enrollment key.
- **st.button**: "Enroll/Re-enroll" button to process the enrollment key.
- **st.button**: "View Class" button next to each enrolled class to navigate to Page 2.
- **st.button**: "Soft Unenroll" button for each enrolled class to initiate soft unenrollment.
- **Feedback Elements**: Use `st.success`, `st.error`, `st.warning` to display messages from `st.session_state.feedback_messages`.

### Functionality
- Fetch enrolled classes from the service layer on load.
- On "Enroll/Re-enroll" button click: Validate enrollment key via service layer, update enrollment, and set feedback messages.
- On "View Class" button click: Set `selected_class` in session state and switch `current_page` to "class_details".
- On "Soft Unenroll" button click: Call service layer for soft unenrollment, update display, and set feedback messages.

### Routing Behavior
- Default page on app start.
- Navigate to Page 2 by setting `current_page` to "class_details" and storing `selected_class`.

## Page 2: Class Details
This page provides detailed information about a selected class.

### Layout and Elements
- **st.title**: "Class Details"
- **st.container**: Wrap the content.
- **st.columns**: Use columns to display class information and actions.
- Display selected class information (e.g., Course Name, Description, Instructor) fetched from service layer.
- Show course details (e.g., Schedule, Prerequisites).
- Display enrollment status (e.g., "Enrolled", "Not Enrolled").
- **st.button**: "Return to Dashboard" to navigate back to Page 1.
- **Feedback Elements**: Display any relevant messages from `st.session_state.feedback_messages`.

### Functionality
- Load class details and enrollment status using `selected_class` from session state.
- Minimal interactions; primarily informational.

### Routing Behavior
- Accessible only when `current_page` is "class_details".
- Navigate back to Page 1 by setting `current_page` to "dashboard" and clearing `selected_class`.

## Routing Behavior
- Use conditional rendering based on `st.session_state.current_page`.
- On app rerun, check `current_page` to display the appropriate page.
- Ensure navigation buttons update session state accordingly.

## Feedback Behavior
- Store messages in `st.session_state.feedback_messages` as a list of dictionaries (e.g., [{"type": "success", "message": "Enrolled successfully"}]).
- Display messages at the top or bottom of each page using appropriate Streamlit elements (`st.success`, `st.error`, `st.warning`).
- Clear messages after display or on successful actions to avoid persistence.

## Soft-Unenroll Flow Behavior
- On "Soft Unenroll" button click in Page 1:
  - Call service layer method to perform soft unenrollment (update status without full removal).
  - Refresh enrolled classes list.
  - Set success/error feedback based on service response.
- Soft unenrollment allows students to temporarily withdraw while preserving some data, as per backend logic.

## Service Layer Integration
- Call existing service methods for:
  - Fetching enrolled classes.
  - Validating and processing enrollment keys.
  - Retrieving class details.
  - Handling soft unenrollment.
- Make minimal changes to the database layer; rely on service methods to handle data operations.

## Additional Notes
- Ensure the UI is responsive and user-friendly.
- Handle edge cases like invalid enrollment keys or non-existent classes with appropriate error messages.
- Test session state persistence across page navigations.