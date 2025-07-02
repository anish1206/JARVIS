import streamlit as st

# App title
st.set_page_config(page_title="GeoAssist Chatbot", page_icon="🛰️")
st.title("🛰️ GeoAssist - Satellite Data Help Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_query = st.chat_input("Ask something about satellite data...")
if user_query:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Dummy bot response for now (we'll connect it to NLP later)
    bot_response = "I'm processing your question... (response logic coming soon)"
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)
