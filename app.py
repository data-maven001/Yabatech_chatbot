import streamlit as st  # Interface
import pandas as pd
from rapidfuzz import process, fuzz  # For fuzzy matching

# --- Page Configuration ---
st.set_page_config(
    page_title="Yabatech EduBot",
    page_icon="assets/YABATECH-LOGO.png",  # ✅ Fixed typo: 'assests' -> 'assets'
    layout="centered"
)

# --- Initialize Session State ---
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Load Knowledge Base from Google Sheets ---
@st.cache_data(show_spinner=False)
def load_kb():
    try:
        url = "https://docs.google.com/spreadsheets/d/1iuMdndmSVkq8JR6Ir42s29-_3QHcGOX6/export?format=csv"
        df = pd.read_csv(url)
        return dict(zip(df['Question'].str.lower(), df['Answer']))
    except Exception as e:
        st.error(f"⚠️ Could not load knowledge base: {e}")
        return {}

# --- Fuzzy Matching Logic ---
def get_best_match(question, kb, threshold=70):
    questions = list(kb.keys())
    match, score, _ = process.extractOne(question.lower(), questions, scorer=fuzz.token_sort_ratio)
    if score >= threshold:
        return kb[match], score
    return "Hmm 🤔 I'm not sure I understand. Could you rephrase?", score

# --- Welcome Page Layout ---
def welcome_page():
    st.markdown("### 🎓 Welcome to Yabatech EduBot")
    st.image("assets/YABATECH-LOGO.png", width=200)  # ✅ Fixed typo
    st.subheader("Your Digital Learning Assistant")
    st.markdown("""
        🚀 *Yabatech EduBot helps you with:*
        - School admissions and processes  
        - Course guidance and academic support  
        - FAQs about payments, hostels, resumption, etc.  
        
        Just click the button below to start chatting!
    """)
    if st.button("Start Chatbot 💬"):
        st.session_state.page = "chatbot"
        st.rerun()

# --- Chatbot Page Logic ---
def chatbot_page():
    qa_dict = load_kb()

    # Header with logo
    col1, col2 = st.columns([1, 12])
    with col1:
        st.image("assets/YABATECH-LOGO.png", width=50)
    with col2:
        st.markdown("<h1 style='padding-top: 5px;'>Yabatech EduBot</h1>", unsafe_allow_html=True)
    st.caption("Ask your question below:")

    # Display chat history
    for speaker, message in st.session_state.chat_history:
        with st.chat_message(name=speaker.lower()):
            st.markdown(f"**{speaker}:** {message}")

    # Chat Input Box
    user_input = st.chat_input("Ask your question here...")

    if user_input:
        st.session_state.chat_history.append(("You", user_input))

        with st.spinner("EduBot is thinking..."):
            reply, _ = get_best_match(user_input, qa_dict)
        st.session_state.chat_history.append(("EduBot", reply))
        st.rerun()

    # Control Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔙 Return Home"):
            st.session_state.page = "welcome"
            st.rerun()
    with col2:
        if st.button("🧹 Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("---")
    st.markdown("📬 Contact: [support@yabatech.edu.ng](mailto:support@yabatech.edu.ng)")
    st.markdown("🔒 Powered by YDTA AI/ML Project | Built with ❤️ using Streamlit")

# --- Page Control ---
if st.session_state.page == "welcome":
    welcome_page()
else:
    chatbot_page()
