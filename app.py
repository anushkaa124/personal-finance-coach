import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# ─── Load & configure Gemini API key ─────────────────────────────────────────
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

# ─── Page config & custom CSS ────────────────────────────────────────────────
st.set_page_config(
    page_title="Personal Finance Coach 💰",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    /* 1. Full‑page background */
    .reportview-container, .main {
      background: #eef2f7;        /* soft light blue/gray */
    }

    /* 2. Override default padding */
    .main .block-container {
      padding-top: 1rem;
      padding-left: 2rem;
      padding-right: 2rem;
    }

    /* 3. Heading styles */
    h1 {
      color: #2c3e50;             /* dark slate */
      font-family: 'Segoe UI', Tahoma, sans-serif;
    }
    h4 {
      color: #34495e;             /* deep slate */
      font-family: 'Segoe UI', Tahoma, sans-serif;
    }

    /* 4. Chat bubble styles */
    .user-bubble {
      background-color: #c8e6c9;
      color: #000;
      padding: 12px;
      border-radius: 15px 15px 0 15px;
      margin: 5px 0;
      text-align: right;
    }
    .coach-bubble {
      background-color: #e3f2fd;
      color: #000;
      padding: 12px;
      border-radius: 15px 15px 15px 0;
      margin: 5px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ─── Sidebar: Quick Topics & Instructions ────────────────────────────────────
st.sidebar.title("🚀 Quick Topics")
common_topics = [
    "Budget Planning", "Savings Strategy", "Investment Options", 
    "Debt Repayment", "Emergency Fund", "Retirement Planning",
    "Expense Tracking", "Credit Score"
]
selected = st.sidebar.radio("Pick a topic:", common_topics)

st.sidebar.markdown("---")
with st.sidebar.expander("💡 How to use"):
    st.write(
        """
        1. Select a topic or type your own question.  
        2. Click **Get Advice**.  
        3. See your personalized finance guidance instantly!
        """
    )

# ─── Main Header ────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 4])

with col2:
    st.markdown("<h1>Personal Finance Coach</h1>", unsafe_allow_html=True)
    st.markdown("<h4>Built by Anushka 12319243, Grainy 12316766</h4>", unsafe_allow_html=True)

st.write("---")
st.write("💬 Chat with your finance coach below:")

# ─── Initialize chat history ─────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ─── Get user input ──────────────────────────────────────────────────────────
user_msg = st.text_input("Your question:", value=selected, key="input")

if st.button("Get Advice") and user_msg:
    prompt = (
        "You are a friendly, expert personal finance coach. "
        f"Provide clear, actionable advice on: {user_msg}"
    )
    with st.spinner("Thinking… 🤔"):
        try:
            res = model.generate_content(prompt)
            coach_reply = res.text.strip()
        except Exception as e:
            coach_reply = f"Error: {e}"

    # Save to history
    st.session_state.history.append(("You", user_msg))
    st.session_state.history.append(("Coach", coach_reply))

# ─── Render Chat Bubbles ─────────────────────────────────────────────────────
for sender, msg in st.session_state.history:
    if sender == "You":
        st.markdown(f"<div class='user-bubble'><b>You:</b> {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='coach-bubble'><b>Coach:</b> {msg}</div>", unsafe_allow_html=True)

# ─── Reset Chat ─────────────────────────────────────────────────────────────
if st.button("🔄 Reset Chat"):
    st.session_state.history = []
    st.rerun()
