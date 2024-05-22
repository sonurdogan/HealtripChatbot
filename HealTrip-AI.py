import streamlit as st
import os
from dotenv import load_dotenv
from healtrip_chatbot_rag import run_healtrip_chatbot
from healtrip_chatbot_rag import start_vector_store
from healtrip_chatbot_rag import create_vector_store

load_dotenv()
# configure password
PASSWORD = os.environ["UI_PASS"]

st.set_page_config("Healtrip AI")
st.title("Welcome to Healtrip Chat Assistant! 👋")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)

password = st.experimental_get_query_params().get("pass", [""])[0]
if password != PASSWORD:
    st.error("Oops! You seem to be in the wrong place. You are not authorized to view this page.")
    st.stop()

st.markdown(
    """
    This is QA Chat Assistant for Healtrip AI. You can ask anything related to Hospitals and Doctors in the Healtrip.

    With this chat assistant you can plan your trip to the hospital, get information about the doctors, and much more.
    """
    )


if st.sidebar.button("New chat :page_with_curl:"):

    st.session_state.messages = []
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Welcome to HealTrip AI - your personal Healtrip Assistant! 👋"
        }
    ]
if st.sidebar.button("Get the latest version! :rocket:"):
    st.session_state.messages = []
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Welcome to HealTrip AI - your personal Healtrip Assistant! 👋"
        }
    ]
    st.write("Getting the latest version of the database... ⏳")
    created_db = create_vector_store("dhh_db")
    st.write("The latest version of the database has been created successfully! 🎉")
    st.session_state.messages = []
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Welcome to HealTrip AI - your personal Healtrip Assistant! 👋"
        }
    ]

vector_db = start_vector_store("dhh_db")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"assistant",
            "content":"Welcome to HealTrip AI - your personal Healtrip Assistant! 👋"
        }
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process and store Query and Response
def llm_function(query):
    response = run_healtrip_chatbot(query, vector_db)

    # Displaying the Assistant Message
    with st.chat_message("assistant"):
        st.markdown(response)

    # Storing the User Message
    st.session_state.messages.append(
        {
            "role":"user",
            "content": query
        }
    )

    # Storing the User Message
    st.session_state.messages.append(
        {
            "role":"assistant",
            "content": response
        }
    )

# Accept user input
query = st.chat_input("")

# Calling the Function when Input is Provided
if query:
    # Displaying the User Message
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(query)


