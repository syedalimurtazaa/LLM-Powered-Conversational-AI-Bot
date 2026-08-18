<h1 align="center">🤖 Rule-Based Chatbot</h1>

<p align="center">
  A beginner-friendly Python chatbot powered by simple keyword matching.
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&duration=2500&pause=900&color=0E75B6&center=true&vCenter=true&width=600&lines=Python+Rule-Based+Chatbot;Keyword+Matching+%7C+Random+Replies;No+APIs+%7C+No+External+Libraries" alt="Typing SVG" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3" />
  <img src="https://img.shields.io/badge/Type-Beginner%20Project-22C55E?style=for-the-badge" alt="Beginner Project" />
  <img src="https://img.shields.io/badge/Dependencies-None-F59E0B?style=for-the-badge" alt="No Dependencies" />
</p>

<br/>

## ✨ About the Project

This is a simple **rule-based chatbot** made with Python. It responds to users by identifying keywords in their messages and selecting a suitable random reply.

It is designed as a beginner project to demonstrate Python dictionaries, functions, loops, conditions, user input, and the `random` module.

<br/>

## 🚀 Features

- 👋 Greetings and farewells
- 💬 “How are you?” conversations
- 🤖 Bot name, age, and creator questions
- 🙋 User-name responses
- 🆘 Help and thank-you messages
- 😊 Good and bad mood replies
- 😂 Random programming jokes
- 🎲 Randomized responses
- ❓ Fallback response for unknown messages
- 🚪 Clean exit using `bye`, `goodbye`, `exit`, or `quit`
- 📊 Session summary with total messages exchanged

<br/>

## 🛠️ Tech Stack

<p align="left">
  <img src="https://skillicons.dev/icons?i=python" alt="Python" />
  <img src="https://img.shields.io/badge/Standard%20Library-random-3776AB?style=flat-square&logo=python&logoColor=white" height="48" alt="Random module" />
</p>

<br/>

## 📁 Project Structure

```text
rule-based-chatbot/
│
├── chatbot_beginner.py
├── requirements.txt
└── README.md
```

<br/>

## ▶️ Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd rule-based-chatbot
```

### 2. Run the chatbot

```bash
python chatbot_beginner.py
```

> Python 3 is required. No external packages need to be installed.

<br/>

## 💬 Example Conversation

```text
ChatBuddy: Hello! Type 'help' for ideas or 'bye' to exit.

You: hi
ChatBuddy: Hi! Nice to hear from you.

You: what's your name
ChatBuddy: I'm ChatBuddy, your friendly rule-based chatbot.

You: tell me a joke
ChatBuddy: Why do programmers prefer dark mode? Because light attracts bugs!

You: bye
ChatBuddy: Goodbye! Have a great day.

(Session summary: you sent 4 message(s). Goodbye!)
```

<br/>

## ⚙️ How It Works

```text
User Input
    ↓
Convert text to lowercase
    ↓
Match input with keywords
    ↓
Select a random response
    ↓
Display reply or fallback message
```

1. `KEYWORDS` stores topics and trigger words.
2. `RESPONSES` stores multiple replies for every topic.
3. The chatbot checks the user's message for matching keywords.
4. `random.choice()` selects a different response when possible.
5. The chat ends when an exit keyword is detected.

<br/>

## 📚 Learning Concepts

- Python dictionaries
- Lists
- Functions
- `while` loops
- `if / elif / else` conditions
- User input with `input()`
- Random responses using `random.choice()`

<br/>
