from uagents import Agent, Context, Model

# Define the message model
class Dream(Model):
    description: str

# Create the User Agent
user_agent = Agent(name="User", seed="user_seed", port=8001, endpoint=["http://127.0.0.1:8001/submit"])

@user_agent.on_event("startup")
async def send_dream(ctx: Context):
    dream_text = input("Describe your dream: ")
    print("Sending your dream to Dreamie...")

    dreamie_address = "agent1qtu6wt5jphhmdjau0hdhc002ashzjnueqe89gvvuln8mawm3m0xrwmn9a76"  # Replace with actual address from dream_agent.py logs

    success = await ctx.send(dreamie_address, Dream(description=dream_text))
    
    if success:
        print("✅ Dream sent successfully!")
    else:
        print("❌ Failed to send the dream. Ensure Dreamie is running!")

@user_agent.on_message(model=Dream)
async def receive_interpretation(ctx: Context, sender: str, dream: Dream):
    print(f"\n🌙 Dreamie interprets: {dream.description}")

if __name__ == "__main__":
    print("Starting User Agent...")
    user_agent.run()

