import openai
import os
from uagents import Agent, Context, Model

# Load OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Tutor Agent
tutor = Agent(name="Tutor", seed="tutor_secret_seed", port=8000, endpoint=["http://127.0.0.1:8000/submit"])

# Define a message model for student questions
class Question(Model):
    text: str

# Define a message model for answers
class Answer(Model):
    text: str

# Function to get response from OpenAI
def get_gpt_answer(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a knowledgeable tutor."},
                  {"role": "user", "content": question}]
    )
    return response["choices"][0]["message"]["content"]

@tutor.on_event("startup")
async def start_tutor(ctx: Context):
    ctx.logger.info(f"Hello, I am {tutor.name}, your AI Tutor!")
    ctx.logger.info(f"My address: {tutor.address}")

@tutor.on_message(model=Question)
async def answer_question(ctx: Context, sender: str, question: Question):
    ctx.logger.info(f"Received question from {sender}: {question.text}")
    answer_text = get_gpt_answer(question.text)

    # Send back the answer
    await ctx.send(sender, Answer(text=answer_text))

if __name__ == "__main__":
    tutor.run()
