from uagents import Agent, Context, Model
import random

# Create an AI Dream Interpreter agent
dreamie = Agent(name="Dreamie", seed="secret_seed_phrase", port=8000, endpoint=["http://127.0.0.1:8000/submit"])

# Define a message model for dream descriptions
class Dream(Model):
    description: str

# Sample dream interpretations
interpretations = [
    "Your dream suggests you're on the verge of a big breakthrough! Keep pushing forward!",
    "Flying in your dream? You crave freedom and adventure! Maybe it's time for a spontaneous trip!",
    "Seeing a mysterious figure? Your subconscious is telling you to embrace the unknown!",
    "Dreaming about falling? You might be feeling out of control in some aspect of your life—time to take charge!",
    "Did you dream of talking animals? Your intuition is trying to communicate something important!"
]

@dreamie.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Hello, I'm {dreamie.name}, your AI Dream Interpreter!")
    ctx.logger.info(f"My address: {dreamie.address}")  # Print address

@dreamie.on_message(model=Dream)
async def interpret_dream(ctx: Context, sender: str, dream: Dream):
    interpretation = random.choice(interpretations)
    ctx.logger.info(f"User {sender} shared a dream: {dream.description}")
    
    # Send back the interpretation
    await ctx.send(sender, Dream(description=interpretation))

if __name__ == "__main__":
    dreamie.run()
