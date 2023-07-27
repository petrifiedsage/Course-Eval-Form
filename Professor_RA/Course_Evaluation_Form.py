import streamlit as st
import pandas as pd


def main():
    st.set_page_config(initial_sidebar_state="collapsed")
    st.title("Course Evaluation Form")
    student_df = pd.read_csv("cs_students.csv")
    student_id = st.selectbox("Select your Student ID", student_df["StudentID"].tolist())
    st.code(f"Name: {student_df[student_df['StudentID'] == student_id]['Name'].values[0]}", language="markdown")
    professor_df = pd.read_csv("cs_professor.csv")
    professor_name = st.selectbox("Select your Course ", professor_df["Subject"].tolist())
    professor_id = professor_df[professor_df["Subject"] == professor_name]["CourseID"].values[0]
    st.code(f"Instructor: {professor_df[professor_df['Subject'] == professor_name]['PName'].values[0]}",
            language="markdown")
    feedback_df = pd.read_csv("cs_feedback.csv")
    review_already_exists = ((feedback_df["StudentID"] == student_id) &
                             (feedback_df["ProfessorID"] == professor_id)).any()

    if not review_already_exists:
        st.write("")
        st.write("")
        widget1_placeholder, widget2_placeholder, widget3_placeholder, widget4_placeholder, widget5_placeholder, \
            widget6_placeholder, widget7_placeholder, widget8_placeholder, widget9_placeholder, widget10_placeholder \
            = [st.empty() for _ in range(10)]
        widget_placeholder_list = [widget1_placeholder, widget2_placeholder, widget3_placeholder, widget4_placeholder,
                                   widget5_placeholder, widget6_placeholder, widget7_placeholder, widget8_placeholder,
                                   widget9_placeholder, widget10_placeholder]
        st.write()
        widget1_placeholder.code("Ratings\n1 - Unsatisfactory\n2 - Needs Improvement\n3 - Average\n4 - Good\n5 - "
                                 "Excellent\n", language="markdown")

        r1 = widget2_placeholder.select_slider("Instructors Effectiveness", range(1, 6), value=3)
        r2 = widget3_placeholder.select_slider("Assignments and Assessment", range(1, 6), value=3)
        r3 = widget4_placeholder.select_slider("Instructors Overall Communication", range(1, 6), value=3)
        r4 = widget5_placeholder.select_slider("Instructors Availability and Support", range(1, 6), value=3)
        r5 = widget6_placeholder.select_slider("Classroom Environment", range(1, 6), value=3)
        r6 = widget7_placeholder.select_slider("Course Content", range(1, 6), value=3)
        r7 = widget8_placeholder.select_slider("Overall Course Effectiveness", range(1, 6), value=3)
        comment = widget9_placeholder.text_area("comment", label_visibility="hidden",
                                                placeholder="Please share your feedback")
        submit_button = widget10_placeholder.button("SUBMIT")

        if submit_button:
            if comment != "":
                feedback_df = pd.read_csv("cs_feedback.csv")
                feedback_df.loc[len(feedback_df)] = \
                    [student_id, professor_df[professor_df['Subject'] == professor_name]['CourseID'].values[0],
                     comment.replace("\n", " "), r1, r2, r3, r4, r5, r6, r7]
                feedback_df.to_csv("cs_feedback.csv", index=False)

                for widget_placeholder in widget_placeholder_list:
                    widget_placeholder.empty()

                st.info("Review submitted successfully")
                st.experimental_rerun()
            else:
                st.error("Feedback not entered")
    else:
        st.write("")
        st.code("Review submitted", language="markdown")


if __name__ == "__main__":
    main()
