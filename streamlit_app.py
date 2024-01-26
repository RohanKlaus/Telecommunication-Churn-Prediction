import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from joblib import load

import sklearn
print(sklearn.__version__)

class SessionState:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

loaded_model = load('Telecomchurn.h5')

# Initialize session state
session_state = SessionState(show_result=False)

# Define the input fields along with their corresponding input types and conditions
input_columns = {
    'voice_plan': {'type': 'radio', 'options': ['NO', 'YES'], 'text': 'Do you have a voice plan?'},
    'voice_messages': {'type': 'number_input', 'text': 'Enter the number of voice messages'},
    'intl_plan': {'type': 'radio', 'options': ['NO', 'YES'], 'text': 'Do you have an international plan?'},
    'intl_mins': {'type': 'number_input', 'text': 'Enter international duration(min)'},
    'intl_calls': {'type': 'number_input', 'text': 'Enter the number of international calls'},
    'intl_charge': {'type': 'number_input', 'text': 'Enter international charges'},
    'day_mins': {'type': 'number_input', 'text': 'Enter daytime duration(min)'},
    'day_charge': {'type': 'number_input', 'text': 'Enter daytime charges'},
    'eve_mins': {'type': 'number_input', 'text': 'Enter evening duration(min)'},
    'eve_charge': {'type': 'number_input', 'text': 'Enter evening charges'},
    'night_mins': {'type': 'number_input', 'text': 'Enter nighttime duration(min)'},
    'night_charge': {'type': 'number_input', 'text': 'Enter nighttime charges'},
    'customer_calls': {'type': 'number_input', 'text': 'Enter the number of customer calls'},
}
# Create a dictionary to store user input
user_input = {}

# First page layout
st.title("Telecom Churn Prediction")


# Collect user inputs on the first page
for col, input_info in input_columns.items():
    if input_info['type'] == 'number_input':
        user_input[col] = st.number_input(f"{input_info['text']}", value=0, step=1)
    elif input_info['type'] == 'radio':
            # Map 'NO' to 0 and 'YES' to 1
        user_input[col] = 1 if st.radio(f"{input_info['text']}", options=input_info['options'], key=col) == 'YES' else 0

# Predict button
if st.button("Predict"):
    # Create a DataFrame from user input
    input_df = pd.DataFrame([user_input])
    print(input_df, "input_df")
# Make prediction
prediction = loaded_model.predict(pd.DataFrame([user_input]))[0]

# Set the session state variable to True to show the second page
session_state = SessionState(show_result=True)

# Check if the button to show the second page is clicked
if session_state.show_result:
    # Page break
    st.markdown("---")
    
   # Second page layout
    st.title("Result")

# Display result with animation or other visualizations
if prediction == 1:
    st.markdown("This customer is likely to <span style='color:red; font-size:32px;'>CHURN</span>", unsafe_allow_html=True)
    st.image('https://i.gifer.com/3Qxw.gif', caption=" ", width=500)
else:
    st.markdown("This customer is likely to <span style='color:red; font-size:32px;'>NOT CHURN</span>", unsafe_allow_html=True)
    st.image("https://i.gifer.com/5dk.gif", caption=" ", width=500)
