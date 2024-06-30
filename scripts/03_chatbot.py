import streamlit as st
from hugchat import hugchat
from hugchat.login import Login


# Store LLM generated responses
def get_session_state():
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "How may I help you?"}
        ]
    return st.session_state.messages


# Function for generating LLM response
def generate_response(prompt_input, email, passwd):
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    # Create Chatbot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt_input)


def main():
    # App title
    st.title("Simple ChatBot")

    # Hugging Face Credentials
    with st.sidebar:
        st.title("Login HugChat")
        hf_email = st.text_input("Enter E-mail: ")
        hf_pass = st.text_input("Enter Password: ", type="password")
        if not (hf_email and hf_pass):
            st.warning("Please enter your account!")
        else:
            st.success("Proceed to entering your prompt message!")

    messages = get_session_state()
    
    # Display chat messages
    for message in messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    # User-provided prompt
    if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )
        with st.chat_message("user"):
            st.write(prompt)
            
    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt, hf_email, hf_pass)
                st.write(response)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)


if __name__ == "__main__":
    main()
