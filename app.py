# Import required libraries
import os
from groq import Groq
import streamlit as st
from datetime import datetime

# Set the Groq API Key
os.environ["GROQ_API_KEY"] = "YOUR_GROQ_API_KEY"  # Replace with your actual API key

# Initialize Groq Client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Define topics for each study plan in arrays
topics_30_days = [
    "Describe a memorable event in your life",
    "Discuss your favorite book and why it impacted you",
    "Explain a time when you overcame a challenge",
    # Add topics up to 30...
]
topics_45_days = topics_30_days + [
    "Describe a goal you wish to achieve",
    "Write about a person who inspires you",
    # Add topics up to 45...
]
topics_60_days = topics_45_days + [
    "Discuss the importance of technology in modern life",
    "Explain the role of education in personal development",
    # Add topics up to 60...
]

# Create a dictionary for easy access to topics based on plan
topics_dict = {
    "30 Days": topics_30_days,
    "45 Days": topics_45_days,
    "60 Days": topics_60_days,
}

# Streamlit UI Setup
st.title("Writing Assistant for IELTS, DET, and TOEFL Preparation")
st.write("A tool to enhance your writing skills with focused, instructor-like feedback.")

# Step 1: Choose Study Plan
st.header("Choose Your Study Plan")
plan = st.selectbox("Select your plan duration:", ["30 Days", "45 Days", "60 Days"])

# Retrieve topics for the selected plan
topics = topics_dict[plan]

# Step 2: Select Current Day
st.subheader("Select Your Current Day")
current_day = st.selectbox("Select your current day:", list(range(1, len(topics) + 1)))
st.write(f"**Current Topic for Day {current_day}:** {topics[current_day - 1]}")

# Step 3: Show Upcoming Topics
st.subheader("Upcoming Topics")
upcoming_topics = topics[current_day:] if current_day < len(topics) else []
st.write(upcoming_topics if upcoming_topics else "No more upcoming topics for this plan.")

# Step 4: Input for Essay
st.subheader("Write your essay")
user_essay = st.text_area("Enter your essay here:", height=300)

# Define updated feedback prompt template for concise instructor-like feedback
feedback_prompt_template = """
    You are an experienced English instructor with a focus on providing direct, constructive feedback. Instead of giving vague 
    suggestions, you give specific, actionable advice such as "replace this with this" or "use this phrase for clarity." Focus 
    on grammar, vocabulary, sentence structure, and cohesion. Avoid lengthy explanations—keep the feedback concise and targeted 
    at improvements that will make the writing clearer, more cohesive, and grammatically correct.

    Only address errors or areas where improvement is needed, avoiding unnecessary comments. Adjust feedback based on the user's 
    English proficiency level (A1 to C1), and provide practical examples to improve the student's writing. Use a clear, academic 
    tone without over-explaining.
    """

# Submit Button
if st.button("Submit for Feedback"):
    if user_essay.strip() == "":
        st.error("Please write an essay before submitting.")
    else:
        # Define feedback prompt using user's essay
        feedback_prompt = feedback_prompt_template + f"\n\nEssay: {user_essay}"

        # Call Groq API to generate feedback
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": feedback_prompt}],
            model="llama3-8b-8192"
        )
        feedback = chat_completion.choices[0].message.content

        # Display feedback
        st.subheader("Feedback:")
        st.write(feedback)

# Optional: Plan Information for Motivation
st.sidebar.header("Your Study Plan")
st.sidebar.write(f"You have selected a **{plan}** study plan.")
st.sidebar.write("Each day, complete the essay for the topic provided to enhance your writing skills.")
st.sidebar.write("You will receive targeted feedback to help you improve step by step.")
