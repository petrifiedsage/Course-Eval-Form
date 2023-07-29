# Course Evaluation Platform
The Course Evaluation Platform is a Streamlit web application that enables students to review their courses and provide ratings on various aspects like course content, instructor's effectiveness, class environment,etc. It also allows students to leave comments about their particular course. This application also includes a dashboard that analyzes the ratings using a radar plot and performs sentiment analysis on the received comments.

[Project Link](https://courseevalform.azurewebsites.net/)

  
## Python Packages
* streamlit
* pandas
* matplotlib
* numpy
* azure

## Azure Services
* Azure Web Apps
* Azure Cognitive Services - Language

## Features
* Course Selection: Students can select the specific course they want to evaluate from a list of available courses, ensuring targeted and relevant feedback.
* Evaluation Criteria: The platform provides a set of predefined evaluation criteria, such as course content, instructor effectiveness, teaching methodologies, assignments, and classroom environment. These criteria can be customized to suit the specific needs of the institution.
* Rating System: Students can rate each evaluation criterion on a numerical scale or provide qualitative feedback to capture nuanced opinions.
* Anonymous Feedback: The Course Evaluation Platform ensures anonymity, allowing students to provide honest and constructive feedback without fear of identification.
* Interactive Interface: The platform offers an intuitive and user-friendly interface, making it easy for students to navigate and complete the evaluation process efficiently.
* Sentiment Analysis: The app performs sentiment analysis on the comments received from students. This analysis helps in understanding the sentiment polarity of the comments, such as positive, negative, or neutral, providing insights into the overall student sentiment towards their course
* Dark Theme Support: The application provides a dark-themed user interface, enhancing the visual appeal and allowing users to switch between light and dark themes based on their preferences.
* Data Persistence: The student reviews and ratings are saved to a CSV file, ensuring that the data is persistently stored for future analysis and reference.
* Azure Integration: The project utilizes Azure services, including App Services for hosting the web app and Cognitive Services: Language for performing sentiment analysis on student comments.
