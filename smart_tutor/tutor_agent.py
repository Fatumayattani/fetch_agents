import os
import requests
from dotenv import load_dotenv
from uagents import Agent, Context, Model

# Load environment variables
load_dotenv()

# Get API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Smart Tutor Agent
smart_tutor = Agent(name="Smart Tutor", seed="tutor_secret_seed", port=8000, endpoint=["http://127.0.0.1:8000/submit"])

# Define a message model for student questions
class Question(Model):
    text: str

# Define a message model for answers
class Answer(Model):
    text: str

# Function to get response from Gemini API
def fetch_gemini_answer(question):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": question}]}]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        try:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except KeyError:
            return "Sorry, I couldn't process your request."
    else:
        return f"Error {response.status_code}: {response.text}"

@smart_tutor.on_event("startup")
async def start_tutor(ctx: Context):
    ctx.logger.info(f"Hello, I am {smart_tutor.name}, your AI Tutor!")
    ctx.logger.info(f"My address: {smart_tutor.address}")

@smart_tutor.on_message(model=Question)
async def answer_question(ctx: Context, sender: str, question: Question):
    ctx.logger.info(f"Received question from {sender}: {question.text}")
    answer_text = fetch_gemini_answer(question.text)

    # Send back the answer
    await ctx.send(sender, Answer(text=answer_text))

if __name__ == "__main__":
    smart_tutor.run()
