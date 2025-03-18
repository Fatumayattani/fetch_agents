from uagents import Agent, Context, Model

# Define the message model
class Dream(Model):
    description: str

# Create a client agent
client = Agent(name="User", seed="client_seed", port=8001, endpoint=["http://127.0.0.1:8001/submit"])

@client.on_event("startup")
async def send_dream(ctx: Context):
    dream_text = input("Describe your dream: ")
    print("Sending your dream to Dreamie...")

    # Use Dreamie's actual address from the logs
    dreamie_address = "agent1qtu6wt5jphhmdjau0hdhc002ashzjnueqe89gvvuln8mawm3m0xrwmn9a76"  # Replace this

    success = await ctx.send(dreamie_address, Dream(description=dream_text))
    
    if not success:
        print("❌ Failed to send the dream. Make sure Dreamie is running!")

@client.on_message(model=Dream)
async def receive_interpretation(ctx: Context, sender: str, dream: Dream):
    print(f"\n🌙 Dreamie interprets: {dream.description}")

if __name__ == "__main__":
    client.run()
