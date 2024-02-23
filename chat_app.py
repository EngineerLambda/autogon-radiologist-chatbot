import streamlit as st
import requests
import json
import uuid


st.set_page_config(page_title="AI Medic", page_icon="🩺")
st.title("AI Medic")

# Keep the same id for each session
if "id" not in st.session_state:
    st.session_state.id = str(uuid.uuid4())

# Keep the conversation for each session - to be displayed
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun in the same session
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Collect user prompt, if valid, proceed to display and send to chat history for the session
if prompt := st.chat_input("What Radiology questions do you have?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history for the session
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    
    # AI response part, conversation done to autogon
    agent_id = st.secrets["agent_id"]
    url = f"https://api.autogon.ai/api/v1/services/chatbot/{agent_id}/chat/"

    # set payload for request as in autogon docs
    payload = json.dumps({
                            "session_id": st.session_state.id,
                            "question": prompt
                        })
    # also the headers to be sent
    headers = {
                'Content-Type': 'application/json'
            }

    with st.spinner("Generating response"):
        response = requests.request("POST", url, headers=headers, data=payload)

        # process the api response as json and obtain bot_response from the result
        response = response.json()["data"]["bot_response"]
        
        # Display bot response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
