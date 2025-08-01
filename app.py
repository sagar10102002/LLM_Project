import streamlit as st
from PIL import Image
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv
from io import BytesIO
import base64

# ========== Load API Key ==========
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# ========== Page Config ==========
st.set_page_config(page_title="AI Assistant", layout="wide")

# ========== Inject Clean & Responsive CSS ==========
st.markdown("""
    <style>
        body, .main {
            background-color: #f4f6f8;
            font-family: 'Segoe UI', sans-serif;
            color: #2c3e50;
        }

        h1, h2, h3 {
            color: #2c3e50;
        }

        .avatar-container {
            text-align: center;
            margin-top: 10px;
        }

        .avatar-container img {
            border-radius: 50%;
            max-width: 90px;
            height: auto;
            box-shadow: none;
        }

        .avatar-name {
            margin-top: 0.5rem;
            font-size: 14px;
            font-weight: 700;
            background: linear-gradient(90deg, #42a5f5, #7e57c2, #42a5f5);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shimmer 4s linear infinite;
        }

        @keyframes shimmer {
            0% { background-position: 0% center; }
            100% { background-position: 200% center; }
        }

        hr {
            border-top: 1px solid #ccc;
            margin-top: 1rem;
        }

        section[data-testid="stChatInput"] {
            background-color: #fefefe;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }

        .stChatMessage {
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            animation: fadeIn 0.4s ease-in;
            word-wrap: break-word;
        }

        .stChatMessage[data-testid="user"] {
            background-color: #dceefb;
            border-left: 5px solid #1e88e5;
        }

        .stChatMessage[data-testid="assistant"] {
            background-color: #e8f5e9;
            border-left: 5px solid #43a047;
        }

        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 768px) {
            .avatar-container img {
                max-width: 70px;
            }

            .avatar-name {
                font-size: 13px;
            }
        }
    </style>
""", unsafe_allow_html=True)

# ========== Load Avatar ==========
avatar_path = "IMG_20240320_194823_406.png"
if os.path.exists(avatar_path):
    avatar = Image.open(avatar_path)
    buffered = BytesIO()
    avatar.save(buffered, format="PNG")
    avatar_base64 = base64.b64encode(buffered.getvalue()).decode()
else:
    avatar_base64 = None

# ========== Header ==========
col1, col2 = st.columns([8, 1])
with col1:
    st.markdown("## 🤖 LangChain AI Assistant")
    st.markdown("Ask any question and get real-time answers powered by OpenRouter + LangChain.")
with col2:
    if avatar_base64:
        st.markdown(f"""
        <div class="avatar-container">
            <img src="data:image/png;base64,{avatar_base64}" alt="Avatar"/>
            <div class="avatar-name">Mr. SAGAR SHARMA</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ========== LLM Setup ==========
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1"
)

# ========== Session Chat History ==========
if "messages" not in st.session_state:
    st.session_state.messages = []

# ========== User Chat ==========
user_input = st.chat_input("Ask your question here...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        try:
            response = llm.invoke([HumanMessage(content=user_input)])
            st.session_state.messages.append({"role": "assistant", "content": response.content})
        except Exception as e:
            st.error(f"Error: {str(e)}")

# ========== Display Chat ==========
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
