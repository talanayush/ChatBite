import json
import random
import datetime
import streamlit as st
import time
# from memory import SessionManager
from rag_pipeline import get_retrieval_chain

# mem=SessionManager()

#custom styling interface with streamlit
st.set_page_config(
    page_title="🍽️ Foodie Assistant",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
:root {
    --primary-color: #FF5722;
    --secondary-color: #4CAF50;
    --background-color: #FFF8E1;
    --text-color: #333333;
    --accent-color: #FFC107;
}
.stApp { background-color: var(--background-color); }
.main-header {
    color: var(--primary-color);
    font-family: 'Georgia', serif;
    text-align: center;
    margin-bottom: 0;
    padding: 1rem;
    border-bottom: 2px solid var(--accent-color);
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.stChatMessage[data-testid="stChatMessageUser"] {
    background-color: #E3F2FD;
    border-radius: 15px 15px 0 15px;
    padding: 10px 15px;
    margin-bottom: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    border-left: 3px solid #2196F3;
}
.stChatMessage[data-testid="stChatMessageAssistant"] {
    background-color: #F1F8E9;
    border-radius: 15px 15px 15px 0;
    padding: 10px 15px;
    margin-bottom: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    border-left: 3px solid var(--secondary-color);
}
.stChatInput input {
    border-radius: 25px;
    border: 2px solid var(--accent-color);
    padding: 10px 20px;
    font-size: 1.1rem;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}
.stChatInput input:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 8px rgba(255, 87, 34, 0.4);
}
.stButton button {
    border-radius: 20px;
    background-color: var(--primary-color);
    color: white;
    font-weight: bold;
    transition: all 0.3s ease;
    border: none;
    padding: 0.5rem 1rem;
}
.stButton button:hover {
    background-color: #E64A19;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    transform: translateY(-2px);
}
.date-time-container {
    background-color: #fffbe7;
    border-radius: 10px;
    padding: 1rem 0.5rem 0.5rem 0.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(255, 193, 7, 0.08);
}
.sidebar-header {
    color: var(--primary-color);
    font-size: 1.3rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# sidebare and chat history
with st.sidebar:
    st.markdown("<h2 class='sidebar-header'>🍽️ Settings</h2>", unsafe_allow_html=True)
    restaurant_type = st.selectbox(
        "Restaurant Type",
        ["All", "Vegetarian", "Non-Vegetarian", "Cafe", "Fast Food", "Fine Dining"]
    )
    price_range = st.slider("Price Range (₹)", 0, 5000, (100, 1000), step=100)
    if st.button("Clear Chat", key="clear_chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Hello! I'm your friendly Foodie Assistant. Ask me anything about restaurants, dishes, or menu prices in Ghaziabad!"}
        ]
    st.markdown("### 💾 Chat History")
    if "messages" in st.session_state and len(st.session_state.messages) > 1:
        if st.button("Export Chat History", key="export_chat"):
            chat_export = {"messages": st.session_state.messages}
            st.download_button(
                label="Download JSON",
                data=json.dumps(chat_export, indent=2),
                file_name=f"foodie_chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

# main page
st.markdown("<h1 class='main-header'>🍽️ Foodie Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#666;'>Your personal guide to restaurants and cuisines in Ghaziabad</p>", unsafe_allow_html=True)

# date and all
with st.container():
    st.markdown("<div class='date-time-container'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_date = st.date_input("📅 Select Date", datetime.date.today())
    with col2:
        selected_time = st.time_input("🕒 Select Time", datetime.datetime.now().time())
    with col3:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        selected_day = st.selectbox("📆 Select Day", days, index=datetime.date.today().weekday())
    current_date_str = f"{selected_day}, {selected_date.strftime('%B %d, %Y')}, {selected_time.strftime('%I:%M %p')}"
    st.markdown(f"<p style='text-align: center; color: #666;'><b>Selected datetime:</b> {current_date_str}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# calling the rag pipeline
retrieval_chain = get_retrieval_chain()

# qucik questions
st.markdown("### Quick Questions")
quick_questions = [
    "What restaurants are open now?",
    "Show me vegetarian restaurants",
    "Best place for coffee in Ghaziabad?",
    "Where can I get North Indian food?",
    "Affordable lunch options?",
    "Popular dishes in Ghaziabad?"
]
cols = st.columns(3)
for i, question in enumerate(quick_questions):
    col_index = i % 3
    with cols[col_index]:
        if st.button(question, key=f"quick_{i}"):
            if "messages" not in st.session_state:
                st.session_state.messages = []
            response = retrieval_chain.invoke({
                "input": question,
                "current_date": current_date_str
            })
            st.session_state.messages.append({"role": "user", "content": question})
            st.session_state.messages.append({"role": "assistant", "content": response.get("answer")})


if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hello! I'm your friendly Foodie Assistant. Ask me anything about restaurants, dishes, or menu prices in Ghaziabad!"}
    ]
if "feedback" not in st.session_state:
    st.session_state.feedback = {}

#animations
def get_thinking_emojis():
    emoji_sets = [
        ["🤔", "🧐", "🤔", "💭", "💡"],
        ["🔍", "🔎", "👀", "📝", "✅"],
        ["🍽️", "🍴", "🥄", "🍲", "😋"]
    ]
    return random.choice(emoji_sets)

# for the feedback thumbs up and down
for idx, message in enumerate(st.session_state.messages):
    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if message["role"] == "assistant" and idx > 0:
            feedback_col1, feedback_col2, feedback_col3 = st.columns([1, 1, 5])
            with feedback_col1:
                if st.button("👍", key=f"like_{idx}"):
                    st.session_state.feedback[idx] = "positive"
                    st.info("Thank you for your feedback!")
            with feedback_col2:
                if st.button("👎", key=f"dislike_{idx}"):
                    st.session_state.feedback[idx] = "negative"
                    st.info("Thank you for your feedback! We'll try to improve.")


user_input = st.chat_input("Type your restaurant or menu question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🤖"):
        thinking_placeholder = st.empty()
        emojis = get_thinking_emojis()
        for emoji in emojis:
            thinking_placeholder.markdown(f"{emoji} Thinking...")
            time.sleep(0.25)
        response = retrieval_chain.invoke({
            "input": user_input,
            "current_date": current_date_str
        })
        answer = response.get("answer", "Sorry, I couldn't find an answer.")
        thinking_placeholder.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

# fun fact about food
food_facts = [
    "Did you know? The world's hottest chili pepper is the Carolina Reaper.",
    "Fun fact: Pizza was the first food consumed in space when delivered to the International Space Station in 2001.",
    "Interesting: The most expensive pizza in the world costs $12,000 and takes 72 hours to make.",
    "Did you know? The world's oldest known cookbook was written in 1700 BC.",
    "Fun fact: Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly good to eat."
]
st.markdown(f"<p style='text-align: center; font-style: italic; color: #888;'>{random.choice(food_facts)}</p>", unsafe_allow_html=True)
