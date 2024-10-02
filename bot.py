import streamlit as st
from utils import write_message
from agent import generate_response

# Before starting:
# role: human or assistant
# can add save parameter to instruct write_message to append the message to the session state

# Page Config
st.set_page_config("Ebert", page_icon=":movie_camera:")
# configure the title and icon used on the page

# Set up Session State
# The following code block checks the session state for the current user
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm the GraphAcademy Chatbot!  How can I help you?"},
    ]
# the code creates a default list of messages if the session is empty
# write_message() writes messages to the screen

# Submit handler
def handle_submit(message):
    """
    Submit handler:

    You will modify this method to talk with an LLM and provide
    context using data from Neo4j.
    """

    # Handle the response
    with st.spinner('Thinking...'):

        response = generate_response(message)
        write_message('assistant', response)


# Display messages in Session State
for message in st.session_state.messages:
    write_message(message['role'], message['content'], save=False)

# Handle any user input
if question := st.chat_input("What is up?"):
    # Display user message in chat message container
    write_message('user', question)

    # Generate a response
    handle_submit(question)
