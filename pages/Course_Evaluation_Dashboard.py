import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

categories = ['Communication', 'Teaching Effectiveness', 'Clarity and Organization', 'Knowledge and Expertise',
              'Classroom Management', 'Course Materials', 'Availability and Support']


def setup_azure_cognitive_services():
    api_key = "e2c83368bf6b407baa06a4a583c87af2"
    endpoint = "https://courseevaluationsentiment.cognitiveservices.azure.com/"
    credential = AzureKeyCredential(api_key)
    text_analytics_client = TextAnalyticsClient(endpoint, credential)
    return text_analytics_client


def analyze_text_segments(text_analytics_client, text_segments):
    scores = []

    for segment in text_segments:
        response = text_analytics_client.analyze_sentiment(documents=[segment])
        scores.append([response[0]['confidence_scores'].positive, response[0]['confidence_scores'].neutral,
                       response[0]['confidence_scores'].negative])

    return scores


def get_scores(scores):
    sum_of_scores = [sum(sublist) for sublist in zip(*scores)]
    average = [round(total / len(scores), 2) for total in sum_of_scores]
    return average


def get_adjective(value):
    if 0.1 <= value < 0.25:
        return "Insignificantly"
    elif value == 0.25:
        return "Slightly"
    elif 0.25 < value < 0.5:
        return "Mildly"
    elif value == 0.5:
        return "Moderately"
    elif 0.5 < value < 0.75:
        return "Fairly"
    elif value == 0.75:
        return "Significantly"
    elif 0.75 < value < 0.9:
        return "Greatly"
    elif 0.9 <= value <= 1:
        return "Extremely"


def break_string_into_lines(text, limit):
    max_line_length = limit
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_line_length:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            current_line = word

    if current_line:
        lines.append(current_line.strip())

    return "\n".join(lines)


def plot_radar_chart(teacher_ratings):
    plt.style.use("default")
    teacher_ratings = [round(rating, 2) for rating in teacher_ratings]
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.plot(angles, teacher_ratings + [teacher_ratings[0]], color='skyblue', linewidth=2)
    ax.fill(angles, teacher_ratings + [teacher_ratings[0]], color='skyblue', alpha=0.4)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=7)
    ax.set_yticklabels([])
    ax.grid(True)

    for angle, rating in zip(angles[:-1], teacher_ratings):
        ax.text(angle, rating, str(rating), ha='center', va='center')
    return fig


def main():
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
    st.title("Course Evaluation Dashboard")
    professor_df = pd.read_csv("cs_professor.csv")
    professor_name = st.selectbox("Course Name", professor_df["Subject"].tolist(), label_visibility="hidden")
    st.write("")
    st.write("")
    st.write("")
    professor_id = professor_df[professor_df["Subject"] == professor_name]["CourseID"].values[0]
    feedback_df = pd.read_csv("cs_feedback.csv")
    feedback_df = feedback_df[feedback_df["ProfessorID"] == professor_id]

    if not feedback_df.empty:
        emp_col1, col, emp_col2 = st.columns([0.2, 0.8, 0.2])
        avg_professor_rating = [feedback_df["R1"].mean(), feedback_df["R2"].mean(), feedback_df["R3"].mean(),
                                feedback_df["R4"].mean(), feedback_df["R5"].mean(), feedback_df["R6"].mean(),
                                feedback_df["R7"].mean()]

        with col:
            fig = plot_radar_chart(avg_professor_rating)
            st.subheader("Average Ratings")
            st.pyplot(fig)

        col1, empty_col, col2 = st.columns([0.6, 0.1, 0.3])
        text_analytics_client = setup_azure_cognitive_services()

        with col1:
            st.subheader("Reviews")
            col3, col4 = st.columns([0.88, 0.12])

            review_name = st.selectbox("Select review", [f"Review {i}" for i in range(1, len(feedback_df) + 1)])
            comment = feedback_df.iloc[int(review_name[-1:]) - 1]["Feedback"]
            st.code(break_string_into_lines(comment, 84), language="markdown")
            score = analyze_text_segments(text_analytics_client, [comment])[0]
            st.code(f"Positive: {score[0]}\nNeutral: {score[1]}\nNegative: {score[2]}", language="markdown")

        with col2:
            st.subheader("Overall Sentiment")
            reviews = feedback_df["Feedback"].values.tolist()
            scores = analyze_text_segments(text_analytics_client, reviews)
            score = get_scores(scores)
            statement = ""

            if score[0] > score[1] and score[0] > score[2]:
                statement += f"{get_adjective(score[0])} Positive"

                if get_adjective(score[1]):
                    statement += f", {get_adjective(score[1])} Neutral"

                if get_adjective(score[2]):
                    statement += f", {get_adjective(score[2])} Negative"

            elif score[1] > score[0] and score[1] > score[2]:
                statement += f"{get_adjective(score[1])} Neutral"

                if get_adjective(score[0]):
                    statement += f", {get_adjective(score[0])} Positive"

                if get_adjective(score[2]):
                    statement += f", {get_adjective(score[2])} Negative"

            elif score[2] > score[0] and score[2] > score[1]:
                statement += f"{get_adjective(score[2])} Negative"

                if get_adjective(score[0]):
                    statement += f", {get_adjective(score[0])} Positive"

                if get_adjective(score[1]):
                    statement += f", {get_adjective(score[1])} Neutral"

            st.code(break_string_into_lines(statement, 38), language="markdown")
            st.code(f"Positive: {score[0]}\nNeutral: {score[1]}\nNegative: {score[2]}", language="markdown")
            aspects = break_string_into_lines(", ".join([categories[index] for index, value in
                                                         enumerate(avg_professor_rating) if value < 3]), 38)

            if aspects:
                st.write("Aspects to Improve")
                st.code(break_string_into_lines(", ".join([categories[index] for index, value in
                                                           enumerate(avg_professor_rating) if value < 3]), 38),
                        language="markdown")

    else:
        st.info("No reviews submitted")


if __name__ == "__main__":
    main()
