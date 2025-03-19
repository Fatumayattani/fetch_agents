import os
from uagents import Agent, Context, Model
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define message model
class TutorMessage(Model):
    text: str

# Create Student Agent with seed, port, and endpoint
student_agent = Agent(
    name="StudentAgent",
    seed="student_secret_seed",
    port=8002,
    endpoint=["http://127.0.0.1:8002/submit"]
)

# Replace with the actual Tutor Agent Address (Copy from tutor console)
TUTOR_AGENT_ADDRESS = "agent1qt024pv43ckcpmvezps0maw7hqaexa5sakw5qh4xgwvwmpm0at0azpmdxqs"  

@student_agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"🎓 {student_agent.name} is online and ready to learn!")
    ctx.logger.info(f"My address: {student_agent.address}")

    # Send an initial question
    question = "What is the importance of learning Python?"
    ctx.logger.info(f"💬 Sending question to Tutor: {question}")
    await ctx.send(TUTOR_AGENT_ADDRESS, TutorMessage(text=question))

@student_agent.on_message(model=TutorMessage)
async def receive_response(ctx: Context, sender: str, msg: TutorMessage):
    tutor_response = msg.text
    ctx.logger.info(f"📖 Received response from Tutor: {tutor_response}")
    print(f"Tutor: {tutor_response}")

if __name__ == "__main__":
    student_agent.run()
