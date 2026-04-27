import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Database Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #00ff00;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #2b313e;
        border-left: 3px solid #00ff00;
    }
    .bot-message {
        background-color: #1e2128;
        border-left: 3px solid #0099ff;
    }
    .sql-display {
        background-color: #0d1117;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: monospace;
        font-size: 0.9rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_url" not in st.session_state:
    st.session_state.api_url = "http://localhost:8000"

# Sidebar
with st.sidebar:
    st.markdown("## 🤖 AI Database Chatbot")
    st.markdown("---")

    # API Configuration
    st.markdown("### ⚙️ Configuration")
    api_url = st.text_input("API URL", value=st.session_state.api_url)
    if api_url != st.session_state.api_url:
        st.session_state.api_url = api_url

    # Health check
    if st.button("🏥 Health Check"):
        try:
            response = requests.get(f"{st.session_state.api_url}/health")
            if response.status_code == 200:
                st.success("✅ API is healthy!")
                data = response.json()
                st.json(data)
            else:
                st.error("❌ API is not responding")
        except Exception as e:
            st.error(f"❌ Cannot connect to API: {e}")

    st.markdown("---")
    st.markdown("### 📊 Database Schema")
    with st.expander("View Schema"):
        st.markdown("""
        **customers**
        - id, name, email, created_at

        **orders**
        - id, customer_id, order_date, total_amount

        **products**
        - id, name, category, price

        **order_items**
        - id, order_id, product_id, quantity, price
        """)

    st.markdown("---")
    st.markdown("### 💡 Example Questions")
    example_questions = [
        "Show me all customers",
        "Top 5 products by sales",
        "Total revenue by month",
        "Customers with most orders",
        "Average order value"
    ]

    for q in example_questions:
        if st.button(q, key=q):
            st.session_state.example_question = q

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.markdown("<h1 class='main-header'>🤖 AI Database Chatbot</h1>", unsafe_allow_html=True)

# Chat container
chat_container = st.container()

with chat_container:
    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class='chat-message user-message'>
                <strong>👤 You:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='chat-message bot-message'>
                <strong>🤖 Assistant:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)

            # Show SQL if available
            if "sql" in message:
                with st.expander("🔍 View SQL Query"):
                    st.code(message["sql"], language="sql")

            # Show results table if available
            if "results" in message and message["results"]:
                with st.expander(f"📊 View Results ({message['row_count']} rows)"):
                    st.dataframe(message["results"])

# Chat input
st.markdown("---")
user_question = st.text_input(
    "Ask a question about your data:",
    key="user_input",
    value=st.session_state.get("example_question", "")
)

col1, col2 = st.columns([1, 5])
with col1:
    send_button = st.button("🚀 Send", type="primary")

# Clear example question after use
if "example_question" in st.session_state:
    del st.session_state.example_question

# Process user question
if send_button and user_question:
    # Add user message to chat
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    # Show thinking indicator
    with st.spinner("🤔 Processing your question..."):
        try:
            # Call API
            response = requests.post(
                f"{st.session_state.api_url}/chat",
                json={"question": user_question}
            )

            if response.status_code == 200:
                data = response.json()

                # Format bot response
                bot_response = data["explanation"]

                # Add bot message with details
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": bot_response,
                    "sql": data["sql_query"],
                    "results": data["results"],
                    "row_count": data["row_count"],
                    "execution_time": data["execution_time_ms"]
                })

                # Show success message
                st.success(f"✅ Query executed in {data['execution_time_ms']}ms")

            else:
                error_msg = f"❌ Error: {response.json().get('detail', 'Unknown error')}"
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"❌ Connection error: {str(e)}"
            })

    # Rerun to update chat display
    st.rerun()
