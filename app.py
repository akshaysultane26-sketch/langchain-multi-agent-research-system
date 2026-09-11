import streamlit as st
from main import ask_agent

st.set_page_config(page_title="AI Agent Chat", page_icon="🤖")
st.title("🤖 AI Agent Chat")
st.caption("Ask about weather or general topics — powered by Gemini + LangChain")

# Keep chat history across reruns
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input box at the bottom
user_input = st.chat_input("Ask something...")

if user_input:
    # Show user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get agent's response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ask_agent(user_input)
            st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})