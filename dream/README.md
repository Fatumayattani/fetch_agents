# 🌙 Dream Interpreter Agents using Fetch.ai (uAgents) 🚀

This project demonstrates how to create two AI agents that communicate using **Fetch.ai's uAgents framework**. The agents work together to interpret dreams! ✨

## 🤖 AI Agents

- **🧠 Dream Agent** – Acts as an AI dream interpreter.
- **👤 User Agent** – Sends a dream description to the Dream Agent and receives an interpretation.

## 🛠️ Prerequisites

Ensure you have the following installed on your **Ubuntu terminal**:

- ✅ Python 3.8+
- ✅ Poetry (for dependency management)
- ✅ Fetch.ai uAgents library

## 🔧 Setup Instructions

### 1️⃣ Install Poetry (if not installed)
```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
poetry --version  # Verify installation
```

### 2️⃣ Create the Project Folder
```bash
git clone https://github.com/Fatumayattani/fetch_agents.git
cd fetch_agents/dream
```

### 3️⃣ Install Dependencies
```bash
poetry install
```

## 🚀 Running the Agents

### ▶️ Start the Dream Agent
```bash
python dream_agent.py
```
Copy the **agent address** from the logs for the next step and paste it in dream_user file.

### ▶️ Start the User Agent
```bash
python dream_user.py
```
Enter a dream description when prompted and receive an interpretation. 🎭

## ✨ Example Output
```
Describe your dream: I was flying in the sky
🌙 Dreamie interprets: Flying in your dream? You crave freedom and adventure! Maybe it's time for a spontaneous trip!
```

## 🎯 Conclusion

You have successfully built a **multi-agent AI system** using Fetch.ai's uAgents! 🚀 Your **Dream Agent** and **User Agent** can communicate seamlessly, enabling real-time AI-powered dream interpretations.

Happy coding! 🎭✨

