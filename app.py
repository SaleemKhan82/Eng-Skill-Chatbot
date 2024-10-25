# Import required libraries
import os
from groq import Groq
import streamlit as st

# Set the Groq API Key
os.environ["GROQ_API_KEY"] = "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"  # Replace with your actual API key

# Initialize Groq Client
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Define topics for each study plan in arrays
topics_30_days = [
    "Describe a memorable event in your life",
    "Discuss your favorite book and why it impacted you",
    "Explain a time when you overcame a challenge",
    "Describe your favorite place and why you love it",
    "Discuss an important decision you made",
    "Explain the impact of technology on our lives",
    "Write about a hobby that you enjoy",
    "Discuss your goals for the future",
    "Explain a tradition in your culture",
    "Write about a lesson you learned from a failure",
    "Discuss a person you admire and why",
    "Describe a challenging situation you faced",
    "Write about a special family tradition",
    "Discuss an important historical event",
    "Explain the importance of education",
    "Write about your favorite movie and why you love it",
    "Describe your daily routine",
    "Discuss the advantages and disadvantages of social media",
    "Write about a memorable trip you took",
    "Explain a skill you would like to learn",
    "Discuss the role of music in your life",
    "Describe your ideal job and why you want it",
    "Write about a recent achievement you are proud of",
    "Discuss the importance of community service",
    "Explain how you manage stress",
    "Write about your favorite season and why you like it",
    "Discuss the impact of climate change",
    "Explain a cultural difference you've encountered",
    "Write about a book that changed your perspective",
    "Discuss the role of sports in education",
    "Describe a time when you helped someone",
    "Write about a dream you have for the future",
]

topics_45_days = topics_30_days + [
    "Write about a time when you felt proud of yourself",
    "Discuss the importance of teamwork",
    "Explain how to stay motivated during difficult times",
    "Write about a goal you've set for yourself and your progress",
    "Discuss how travel can change a person",
    "Explain the significance of festivals in your culture",
    "Write about a technological advancement you appreciate",
    "Discuss your favorite childhood memory",
    "Explain how you balance work and leisure",
    "Write about an inspiring person in your life",
    "Discuss how to maintain healthy relationships",
    "Write about your dream vacation",
    "Explain the impact of advertising on society",
    "Discuss the importance of mental health",
    "Write about a time you faced a fear",
    "Discuss how you celebrate special occasions",
    "Explain what makes a good leader",
    "Write about a film that inspired you",
    "Discuss the benefits of learning a second language",
    "Explain how you handle conflicts",
    "Write about the role of art in society",
    "Discuss the advantages and disadvantages of online learning",
    "Explain the importance of nutrition in daily life",
    "Write about a recent event in the news that interested you",
    "Discuss your thoughts on public speaking",
    "Explain the significance of honesty",
    "Write about your favorite food and why you love it",
    "Discuss the role of pets in our lives",
    "Explain the impact of social media on relationships",
    "Write about a personal challenge you've overcome",
    "Discuss what makes a good friend",
    "Write about your thoughts on environmental conservation",
]

topics_60_days = topics_45_days + [
    "Discuss how technology has changed education",
    "Explain the effects of globalization",
    "Write about a social issue that concerns you",
    "Discuss the importance of family values",
    "Explain how to create a positive work environment",
    "Write about a life lesson you learned from a mentor",
    "Discuss the benefits of volunteering",
    "Explain how you manage your time effectively",
    "Write about your experience with cultural diversity",
    "Discuss the significance of role models",
    "Explain what you believe is the purpose of life",
    "Write about how to be resilient in difficult times",
    "Discuss the effects of consumerism on society",
    "Explain how art can influence social change",
    "Write about the impact of reading on personal growth",
    "Discuss your thoughts on the future of technology",
    "Explain how to foster creativity in daily life",
    "Write about a cultural event you attended",
    "Discuss the importance of empathy",
    "Explain the benefits of exercise for mental health",
    "Write about the role of government in society",
    "Discuss how to build self-confidence",
    "Explain the significance of lifelong learning",
    "Write about a personal achievement that changed you",
    "Discuss your thoughts on work-life balance",
    "Explain how to cultivate positive habits",
    "Write about the role of innovation in today's world",
    "Discuss the impact of music on culture",
    "Explain how to deal with criticism",
    "Write about your thoughts on artificial intelligence",
    "Discuss how history shapes our present",
    "Explain the importance of self-care",
    "Write about your vision for a better world",
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
st.write("Upcoming Topics:", upcoming_topics if upcoming_topics else "No more upcoming topics for this plan.")

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
