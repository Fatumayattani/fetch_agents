# 🎓 Smart Tutor
<img src="https://img.shields.io/badge/innovationlab-3D8BD3" alt="tag : innovationlab" width="200"/>

This project demonstrates how to create two AI agents that communicate using **Fetch.ai's uAgents framework**. The agents work together
Smart Tutor is an AI-powered tutoring system that enables seamless communication between a student and a tutor agent. The tutor fetches answers using Google's Gemini AI API and provides intelligent responses to student queries.

## 🚀 Features
- 📡 Decentralized agent communication
- 🤖 AI-powered tutor using Gemini API
- 🔄 Real-time Q&A system

## 🛠️ Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Fatumayattani/fetch_agents.git
cd fetch_agents/smart_tutor
```

### 2️⃣ Install Dependencies
Ensure you have [Poetry](https://python-poetry.org/) installed, then run:
```bash
poetry install
```
This will automatically install all required dependencies, including `uagents`.

### 3️⃣ Set Up Environment Variables
Create a `.env` file in the project root and add:
```ini
GEMINI_API_KEY=xxxxxxxxxxxxxx
```

## 🚦 Usage
### 1️⃣ Start the Tutor Agent
```bash
python tutor_agent.py
```
![Tutor output ](assets/tutor1.png)

### 2️⃣ Start the Student Agent
Before running the student agent, make sure you copy-paste the agent address and replace it in the student agent.
```bash
python student_agent.py
```
When you run the student agent, you will be prompted with a question to enter.

![student output ](assets/student1.png)

Type your query and press enter to receive a response from the tutor agent.

![student output ](assets/student2.png)

Tutor will receive the question

![student output ](assets/student3.png)

The tutor fetches answers using Google's Gemini AI API and provides intelligent responses to student queries.

![student output ](assets/student4.png)

Real-time interaction logs showcasing seamless communication between Student and Tutor agents on Agentverse
 
 ![student output ](assets/image11.png)






Both agents are running simultaneously for proper communication. ✅

## ⚙️ How It Works
1. The **Student Agent** sends a question.
2. The **Tutor Agent** receives the question and fetches an answer using the Gemini API.
3. The **Tutor Agent** sends the response back to the Student Agent.

## 📬 Contact
💬 Connect with me on **X (Twitter):** [@fatumayattani](https://twitter.com/fatumayattani)

