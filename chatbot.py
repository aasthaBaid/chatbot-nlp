import os
import json
import datetime
import csv
import nltk
import ssl
import streamlit as st
import random
import re
from collections import Counter
from rapidfuzz import process, fuzz
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold

# Fix SSL issue for nltk downloads
ssl._create_default_https_context = ssl._create_unverified_context
nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt')

# Load intents from JSON
file_path = os.path.abspath("intents.json")
with open(file_path, "r") as file:
    intents = json.load(file)

# Preprocess data
tags, patterns, pattern_to_tag = [], [], {}
for intent in intents:
    for pattern in intent['patterns']:
        tags.append(intent['tag'])
        patterns.append(pattern.lower().strip())
        pattern_to_tag[pattern.lower().strip()] = intent['tag']

# Train model
vectorizer = CountVectorizer()
x = vectorizer.fit_transform(patterns)
y = tags
class_counts = Counter(y)
min_class_size = min(class_counts.values())

if min_class_size < 2:
    clf = LogisticRegression(max_iter=10000, random_state=42).fit(x, y)
else:
    cv_folds = min(5, min_class_size)
    skf = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
    from sklearn.linear_model import LogisticRegressionCV
    clf = LogisticRegressionCV(cv=skf, max_iter=10000, random_state=42).fit(x, y)

def preprocess_text(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text

def chatbot(input_text):
    input_text = preprocess_text(input_text)
    result = process.extractOne(input_text, patterns, scorer=fuzz.WRatio, score_cutoff=80)
    if result is None:
        return "I'm not sure I understand. Can you rephrase? 🤔"
    best_match = result[0]
    input_vector = vectorizer.transform([best_match])
    tag = clf.predict(input_vector)[0]
    for intent in intents:
        if intent['tag'] == tag:
            return random.choice(intent['responses']) + " 😊"
    return "I'm not sure how to respond to that. 🤔"

def main():
    st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")
    
    # Custom CSS for enhanced UI
    st.markdown(
        """
        <style>
        body {background-color: #f0f8ff; color: #333;}
        .stTextInput>div>div>input, .stTextArea>div>textarea {
            font-size: 18px; border-radius: 20px; padding: 15px;
            border: 3px solid #6495ED; background-color: #ffffff; color: #333;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stButton>button {
            font-size: 18px; border-radius: 20px; padding: 15px 30px;
            background: linear-gradient(to right, #6495ED, #4169E1); color: white; border: none;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s;
        }
        .stButton>button:hover {
            transform: translateY(-3px);
        }
        .chat-bubble {
            background: linear-gradient(to right, #E6E6FA, #D8BFD8); padding: 15px; border-radius: 20px;
            display: inline-block; margin: 10px 0; color: #483D8B;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .sidebar .sidebar-content {
            background: linear-gradient(to bottom, #6495ED, #4169E1); color: white;
            border-radius: 10px; padding: 20px;
        }
        .sidebar .sidebar-content a {
            color: white;
        }
        .st-emotion-cache-1y4p8pa {
            padding: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("🤖 Smart AI Chatbot")
    menu = ["Chat", "History", "About"]
    choice = st.sidebar.radio("Menu", menu)
    
    if choice == "Chat":
        st.markdown("### 💬 I can repond to only short forms , and respond with its corresponding full forms!")
        if not os.path.exists('chat_log.csv'):
            with open('chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csv.writer(csvfile).writerow(['User Input', 'Chatbot Response', 'Timestamp'])
        
        user_input = st.text_input("You:")
        if user_input:
            response = chatbot(user_input)
            st.markdown(f'<div class="chat-bubble">🤖 {response}</div>', unsafe_allow_html=True)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('chat_log.csv', 'a', newline='', encoding='utf-8') as csvfile:
                csv.writer(csvfile).writerow([user_input, response, timestamp])
    
    elif choice == "History":
        st.header("📜 Chat History")
        if os.path.exists('chat_log.csv'):
            with open('chat_log.csv', 'r', encoding='utf-8') as csvfile:
                
                csv_reader = csv.reader(csvfile)
                next(csv_reader)
                for row in csv_reader:
                    st.markdown(f'👤 **User:** {row[0]}')
                    st.markdown(f'<div class="chat-bubble">🤖 {row[1]}</div>', unsafe_allow_html=True)
                    st.markdown(f'⏰ **Timestamp:** {row[2]}')
                    st.markdown("---")
            if st.button("🗑️ Delete Chat History"):
                os.remove('chat_log.csv')
                st.success("Chat history deleted successfully!")
        else:
            st.write("No chat history available.")
    
    elif choice == "About":
        st.header("🔍 About AI Chatbot")
        st.write("This chatbot understands and responds to user input using AI-powered NLP.")
        st.markdown("**🚀 Features:**")
        st.markdown("- 🤖 AI-powered natural language understanding")
        st.markdown("- 🎯 Improved accuracy with RapidFuzz and CountVectorizer")
        st.markdown("- 💾 Saves chat history for future reference")
        st.markdown("- 🚀 Responds to the short forms with the full forms")

if __name__ == '__main__':
    main()
