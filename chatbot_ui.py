import streamlit as st
import streamlit.components.v1 as components
import time

# Page config
st.set_page_config(page_title="GeoAssist", layout="wide")

# === Inject Custom HTML + CSS + JS for Animated Stars ===
star_html = """
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      background: #000010;
      margin: 0;
      padding: 0;
      overflow: hidden;
    }
    .stars {
      position: fixed;
      top: 0; left: 0;
      width: 100vw;
      height: 100vh;
      z-index: -1;
    }
    .star {
      position: absolute;
      width: 2px; height: 2px;
      background: white;
      border-radius: 50%;
      animation: twinkle 3s infinite, move 20s linear infinite;
      opacity: 0.6;
    }
    @keyframes twinkle {
      0%, 100% { opacity: 0.2; }
      50% { opacity: 1; }
    }
    @keyframes move {
      0% { transform: translateY(0); }
      100% { transform: translateY(-100vh); }
    }
  </style>
</head>
<body>
  <div class="stars" id="stars"></div>
  <script>
    const stars = document.getElementById('stars');
    for (let i = 0; i < 120; i++) {
      const star = document.createElement('div');
      star.className = 'star';
      star.style.left = Math.random() * 100 + '%';
      star.style.top = Math.random() * 100 + '%';
      star.style.animationDelay = Math.random() * 5 + 's';
      stars.appendChild(star);
    }
  </script>
</body>
</html>
"""

# Inject the starry background
components.html(star_html, height=0)

# === Chatbot UI ===
st.markdown("<h1 style='text-align: center; color: white;'>🌌 GeoAssist Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #bbb;'>Ask anything about satellites, cloud cover, rainfall, or missions.</p>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
query = st.chat_input("Type your question...")

if query:
    st.chat_message("user").markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        msg_placeholder.markdown("GeoAssist is thinking... 🤔")
        time.sleep(1)

        # Placeholder response
        response = "📡 This is a placeholder. Soon, I’ll fetch real satellite data and answers for you!"
        msg_placeholder.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
