"""
app.py
------
An LLM-powered conversational chatbot built with Streamlit + the Groq API.

Features:
  - Uses an LLM (via Groq's fast inference API) to generate responses.
  - Remembers the whole conversation (multi-turn memory).
  - Can call tools: a calculator and a "what's the date/time" lookup.
  - Handles API errors (timeouts, rate limits, bad key, etc.) gracefully.
  - Polished, interactive UI: custom styling, live stats, quick-start
    prompts, a model switcher, and tool-usage badges.

Run with:  streamlit run app.py
"""

import os
import json

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from tools import TOOL_SCHEMAS, TOOL_FUNCTIONS


# =========================================================================
# STEP 1: Configuration
# =========================================================================
load_dotenv()  # reads the .env file and loads GROQ_API_KEY into the environment

# Groq's current production models (see https://console.groq.com/docs/models).
# Shown in the sidebar as a switcher so the person can compare them live.
AVAILABLE_MODELS = {
    "GPT-OSS 120B (smartest)": "openai/gpt-oss-120b",
    "GPT-OSS 20B (fastest)": "openai/gpt-oss-20b",
}
DEFAULT_MODEL_LABEL = "GPT-OSS 120B (smartest)"

SYSTEM_PROMPT = (
    "You are a friendly, helpful assistant. Keep answers concise and clear. "
    "You have access to a calculator tool and a current-date/time tool — "
    "use them whenever a question needs an exact calculation or the "
    "current date/time, instead of guessing the answer yourself."
)

TOOL_DISPLAY_NAMES = {
    "calculator": "🧮 Calculator",
    "get_current_datetime": "🕒 Date/Time",
}

EXAMPLE_PROMPTS = [
    "What's 4562 × 17?",
    "What's today's date?",
    "Explain recursion like I'm 5",
    "Write a haiku about coffee",
]

st.set_page_config(page_title="LLM ChatBot", page_icon="🤖", layout="centered")


# =========================================================================
# STEP 2: Custom styling — makes the default Streamlit look feel more
# like a real product instead of a plain form.
# =========================================================================
st.markdown("""
<style>
    /* Gradient hero header */
    .hero {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
        padding: 1.6rem 1.8rem;
        border-radius: 16px;
        margin-bottom: 1.2rem;
        box-shadow: 0 8px 24px rgba(139, 92, 246, 0.25);
    }
    .hero h1 {
        color: white;
        margin: 0;
        font-size: 1.8rem;
    }
    .hero p {
        color: rgba(255,255,255,0.9);
        margin: 0.3rem 0 0 0;
        font-size: 0.95rem;
    }

    /* Sidebar section cards */
    .sidebar-card {
        background: rgba(139, 92, 246, 0.08);
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: 12px;
        padding: 0.9rem 1rem;
        margin-bottom: 1rem;
    }
    .sidebar-card h4 {
        margin: 0 0 0.5rem 0;
        font-size: 0.95rem;
    }
    .tool-pill {
        display: inline-block;
        background: rgba(139, 92, 246, 0.15);
        border-radius: 999px;
        padding: 0.15rem 0.7rem;
        margin: 0.15rem 0.2rem 0.15rem 0;
        font-size: 0.82rem;
    }

    /* Tool-usage badge under assistant replies */
    .tool-badge {
        display: inline-block;
        background: linear-gradient(135deg, #22c55e22, #16a34a22);
        border: 1px solid #22c55e55;
        color: #22c55e;
        border-radius: 999px;
        padding: 0.15rem 0.7rem;
        font-size: 0.78rem;
        margin-top: 0.4rem;
    }

    /* Quick-prompt buttons: full width, left aligned */
    div[data-testid="stSidebar"] button {
        width: 100%;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================================
# STEP 3: Set up the Groq client (cached so it's only created once)
# =========================================================================
@st.cache_resource
def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)


client = get_client()


# =========================================================================
# STEP 4: Session state — conversation memory + live stats + settings.
# Streamlit re-runs the whole script on every interaction, so anything
# that needs to persist (chat history, counters, chosen model) lives here.
# =========================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []  # [{"role", "content", "tools_used": [...]}]
if "tool_call_count" not in st.session_state:
    st.session_state.tool_call_count = 0
if "model_label" not in st.session_state:
    st.session_state.model_label = DEFAULT_MODEL_LABEL
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


# =========================================================================
# STEP 5: Core function — send the conversation to the LLM, handle any
# tool calls it requests, and return the final text reply + which tools
# were used (so the UI can show a little "used the calculator" badge).
# =========================================================================
def get_bot_response(conversation: list, model_name: str):
    """
    conversation: list of {"role": ..., "content": ...} dicts.
    Returns (reply_text, tools_used_list). Raises on API failure
    (the caller wraps this to handle errors gracefully).
    """
    # conversation may contain extra UI-only fields (like "tools_used" for
    # badges) — the API only accepts "role" and "content", so strip those out.
    clean_conversation = [{"role": m["role"], "content": m["content"]} for m in conversation]
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + clean_conversation

    response = client.chat.completions.create(
        model=model_name,
        messages=api_messages,
        tools=TOOL_SCHEMAS,
        tool_choice="auto",
        max_tokens=1024,
        timeout=30,
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if not tool_calls:
        return response_message.content, []

    assistant_tool_call_msg = {
        "role": "assistant",
        "content": response_message.content or "",
        "tool_calls": [
            {
                "id": tc.id,
                "type": "function",
                "function": {"name": tc.function.name, "arguments": tc.function.arguments},
            }
            for tc in tool_calls
        ],
    }

    tool_result_messages = []
    tools_used = []
    for tc in tool_calls:
        function_name = tc.function.name
        try:
            function_args = json.loads(tc.function.arguments)
        except json.JSONDecodeError:
            function_args = {}

        function_to_call = TOOL_FUNCTIONS.get(function_name)
        result = (f"Error: unknown tool '{function_name}'" if function_to_call is None
                   else function_to_call(**function_args))

        tools_used.append(function_name)
        tool_result_messages.append({
            "role": "tool",
            "tool_call_id": tc.id,
            "name": function_name,
            "content": str(result),
        })

    followup_messages = api_messages + [assistant_tool_call_msg] + tool_result_messages
    final_response = client.chat.completions.create(
        model=model_name, messages=followup_messages, max_tokens=1024, timeout=30,
    )
    return final_response.choices[0].message.content, tools_used


def get_bot_response_safe(conversation: list, model_name: str):
    try:
        return get_bot_response(conversation, model_name)
    except Exception as e:
        error_text = str(e).lower()
        if "rate limit" in error_text or "429" in error_text:
            msg = "⚠️ The API is rate-limited right now (too many requests). Please wait a moment and try again."
        elif "timeout" in error_text or "timed out" in error_text:
            msg = "⚠️ The request timed out. Please try again."
        elif "authentication" in error_text or "api key" in error_text or "401" in error_text:
            msg = "⚠️ Authentication failed — check that GROQ_API_KEY in your .env file is correct and active."
        elif "connection" in error_text:
            msg = "⚠️ Couldn't connect to the API. Check your internet connection and try again."
        else:
            msg = f"⚠️ Something went wrong talking to the model: {e}"
        return msg, []


# =========================================================================
# STEP 6: Sidebar — interactive controls, live stats, quick-start prompts.
# =========================================================================
with st.sidebar:
    st.markdown("### 🤖 LLM ChatBot")

    st.markdown(
        '<div class="sidebar-card"><h4>🛠️ Available tools</h4>'
        '<span class="tool-pill">🧮 Calculator</span>'
        '<span class="tool-pill">🕒 Date/Time</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("#### ⚙️ Model")
    st.session_state.model_label = st.selectbox(
        "Choose which model answers you:",
        options=list(AVAILABLE_MODELS.keys()),
        index=list(AVAILABLE_MODELS.keys()).index(st.session_state.model_label),
        label_visibility="collapsed",
    )

    st.markdown("#### 📊 Session stats")
    col1, col2 = st.columns(2)
    user_turns = sum(1 for m in st.session_state.messages if m["role"] == "user")
    col1.metric("Messages", user_turns)
    col2.metric("Tool calls", st.session_state.tool_call_count)

    st.markdown("#### ⚡ Quick prompts")
    for prompt in EXAMPLE_PROMPTS:
        if st.button(prompt, key=f"quick_{prompt}"):
            st.session_state.pending_prompt = prompt
            st.rerun()

    st.divider()
    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.session_state.tool_call_count = 0
        st.rerun()


# =========================================================================
# STEP 7: Main area — hero header, missing-key check, chat history, input.
# =========================================================================
st.markdown(
    '<div class="hero"><h1>🤖 LLM ChatBot</h1>'
    f'<p>Powered by Groq · <b>{st.session_state.model_label}</b> · '
    'remembers context · can use tools</p></div>',
    unsafe_allow_html=True,
)

if client is None:
    st.error(
        "No GROQ_API_KEY found. Create a `.env` file in this folder with:\n\n"
        "```\nGROQ_API_KEY=your_key_here\n```"
    )
    st.stop()

# Empty-state hint when the conversation hasn't started yet.
if not st.session_state.messages:
    st.info("👋 Say hello, ask a math question, or try a quick prompt from the sidebar!")

# Render the existing conversation so far.
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if message.get("tools_used"):
            badges = " ".join(
                f'<span class="tool-badge">{TOOL_DISPLAY_NAMES.get(t, t)} used</span>'
                for t in message["tools_used"]
            )
            st.markdown(badges, unsafe_allow_html=True)

# A quick-prompt button click, or normal typed input, both flow through here.
user_input = st.chat_input("Type a message...")
if st.session_state.pending_prompt:
    user_input = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input, "tools_used": []})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            model_name = AVAILABLE_MODELS[st.session_state.model_label]
            reply, tools_used = get_bot_response_safe(st.session_state.messages, model_name)
        st.markdown(reply)
        if tools_used:
            st.session_state.tool_call_count += len(tools_used)
            badges = " ".join(
                f'<span class="tool-badge">{TOOL_DISPLAY_NAMES.get(t, t)} used</span>'
                for t in tools_used
            )
            st.markdown(badges, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": reply, "tools_used": tools_used})