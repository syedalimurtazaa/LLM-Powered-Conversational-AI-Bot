<h1 align="center">🚀 LLM-Powered Conversational AI Bot</h1>

<p align="center">
  An advanced AI chatbot built with Groq, Streamlit, multi-turn memory, and tool calling.
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&duration=2500&pause=900&color=0E75B6&center=true&vCenter=true&width=750&lines=LLM-Powered+Conversational+AI;Groq+%7C+Streamlit+%7C+Tool+Calling;Memory+Enabled+AI+Assistant;Fast%2C+Natural%2C+Context-Aware+Responses" alt="Typing SVG" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-Web%20UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Groq-LLM%20Inference-F55036?style=for-the-badge" alt="Groq" />
  <img src="https://img.shields.io/badge/Level-Advanced-8B5CF6?style=for-the-badge" alt="Advanced Project" />
</p>

<br/>

## ✨ About the Project

This project is an advanced conversational AI chatbot powered by the **Groq API**. It uses a real Large Language Model to create natural, context-aware responses while remembering previous messages in the conversation.

The chatbot also supports **tool calling**, allowing the AI to safely perform calculations and retrieve the current date and time.

<br/>

## 🚀 Features

- 🧠 **LLM-powered responses** using Groq
- 💬 **Multi-turn conversation memory**
- 🧮 **Safe calculator tool** using Python's `ast` module
- 🕒 **Real-time date and time lookup**
- 🔧 **AI tool/function calling**
- ⚠️ Friendly handling for API errors, rate limits, bad keys, and timeouts
- 🎨 Polished Streamlit user interface
- 📊 Live sidebar statistics for messages and tool calls
- 🔄 Groq model switcher
- ⚡ One-click quick-start prompts
- ☁️ Ready for deployment on Streamlit Community Cloud

<br/>

## 🛠️ Tech Stack

<p align="left">
  <img src="https://skillicons.dev/icons?i=python" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" height="48" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Groq-LLM%20API-F55036?style=flat-square" height="48" alt="Groq API" />
  <img src="https://img.shields.io/badge/python--dotenv-Environment%20Variables-3776AB?style=flat-square&logo=python&logoColor=white" height="48" alt="python-dotenv" />
</p>

<br/>

## 📁 Project Structure

```text
llm-chatbot/
│
├── app.py              # Streamlit UI, LLM logic, and error handling
├── tools.py            # Calculator and date/time tools
├── requirements.txt
├── .env.example        # API key template
├── .gitignore          # Prevents .env and venv files from being pushed
└── README.md
```

<br/>

## ▶️ Getting Started

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd llm-chatbot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate
```

```bash
# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Your Groq API Key

Copy `.env.example` and rename it to `.env`.

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your API key from [Groq Console](https://console.groq.com/).

### 5. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at:

```text
http://localhost:8501
```

<br/>

## 💬 Example Usage

| User Prompt | What Happens |
|---|---|
| `Hi, who are you?` | The chatbot starts a normal AI conversation. |
| `What's 4562 × 17?` | The AI calls the safe calculator tool. |
| `What's today's date?` | The AI calls the date/time tool. |
| `Tell me a joke about Python.` | The LLM generates a natural response. |
| `Remember that my name is Ali.` | The bot retains this context during the session. |

<br/>

## ⚙️ How It Works

```text
User Message
     ↓
Streamlit Session Memory
     ↓
Groq LLM API + Tool Schemas
     ↓
Does the AI need a tool?
     ↓
 ┌───────────────┴────────────────┐
 ↓                                ↓
No tool needed                 Tool requested
 ↓                                ↓
AI response                   Run local Python tool
 ↓                                ↓
Display answer              Send result back to AI
                                  ↓
                            Display natural answer
```

1. Every user message is saved in `st.session_state.messages`.
2. The full conversation history is sent to Groq on every turn.
3. The LLM decides whether it needs a calculator or date/time tool.
4. When a tool is needed, Python runs it locally and safely.
5. The result is returned to the LLM for a natural-language response.
6. Streamlit displays the conversation, statistics, and tool badges.

<br/>

## 🔐 Security Notes

- The calculator does **not** use Python's `eval()`.
- Expressions are parsed through Python's `ast` module.
- Only approved arithmetic operations are allowed.
- Your API key is stored in `.env`, which should never be uploaded to GitHub.
- The `.gitignore` file protects `.env` and virtual-environment files.

<br/>

## ☁️ Deployment on Streamlit Community Cloud

1. Push this project to GitHub.
2. Visit [Streamlit Community Cloud](https://share.streamlit.io).
3. Sign in using GitHub.
4. Click **New app**.
5. Select your repository, branch, and set `app.py` as the main file.
6. In **Advanced settings → Secrets**, add:

```toml
GROQ_API_KEY = "your_real_groq_api_key_here"
```

7. Click **Deploy**.

Your application will receive a public URL similar to:

```text
https://your-app-name.streamlit.app
```

<br/>
