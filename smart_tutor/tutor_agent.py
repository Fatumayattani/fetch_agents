import os
import openai
from uagents import Agent, Context, Message

# Load OpenAI API key from .env file
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Create Tutor Agent
tutor_agent = Agent(name="TutorAgent")

@tutor_agent.on_message()
async def handle_message(ctx: Context, msg: Message):
    user_question = msg.body
    
    ctx.logger.info(f"Received question: {user_question}")

    # Generate a response using OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a helpful AI tutor."},
                  {"role": "user", "content": user_question}]
    )

    tutor_response = response["choices"][0]["message"]["content"]
    
    # Send response back to the student
    await ctx.send(msg.sender, tutor_response)

# Run the Tutor Agent
if __name__ == "__main__":
    tutor_agent.run()
