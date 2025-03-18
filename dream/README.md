# Dream Interpreter Agents using Fetch.ai (uAgents)

This project demonstrates how to create two AI agents that communicate with each other using **Fetch.ai's uAgents framework**. The agents include:

- **Dream Agent (`dream_agent.py`)** – Acts as an AI dream interpreter.
- **User Agent (`dream_user.py`)** – Sends a dream description to the Dream Agent and receives an interpretation.

## **Prerequisites**

Ensure you have the following installed on your **Ubuntu terminal**:

- Python 3.8+
- Poetry (for dependency management)
- Fetch.ai uAgents library

## **Step 1: Setting Up the Environment (Ubuntu Terminal)**

Since we are working in the **Ubuntu terminal**, we will use **Poetry** for dependency management. If you don’t have Poetry installed, follow these steps:

1. **Install Poetry (if not installed):**
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
   After installation, add Poetry to your PATH:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```
   Verify the installation:
   ```bash
   poetry --version
   ```

## **Step 2: Create the Project Folder**

Create and navigate into the project folder:

```bash
mkdir fetch_agents && cd fetch_agents
```

Initialize a new Poetry environment:

```bash
poetry init
```

When prompted, fill in the details or press Enter to accept defaults.

Then, add **uAgents** to your project:

```bash
poetry add uagents
```

Now, open the project in **VS Code**:

```bash
code .
```

## **Step 3: Creating the Dream Agents**

Inside the **`fetch_agents`** folder, create a new directory called **`dream`** and navigate into it:

```bash
mkdir dream && cd dream
```

Now, create two Python files:

```bash
touch dream_agent.py dream_user.py
```

### **1. Dream Agent (`dream_agent.py`)**

The **Dream Agent** acts as an AI that receives a user's dream description and returns an interpretation.

```python
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
    ctx.logger.info(f"My address: {dreamie.address}")

@dreamie.on_message(model=Dream)
async def interpret_dream(ctx: Context, sender: str, dream: Dream):
    interpretation = random.choice(interpretations)
    ctx.logger.info(f"User {sender} shared a dream: {dream.description}")
    await ctx.send(sender, Dream(description=interpretation))

if __name__ == "__main__":
    dreamie.run()
```

### **2. User Agent (`dream_user.py`)**

The **User Agent** sends a dream description to the **Dream Agent** and receives an interpretation.

```python
from uagents import Agent, Context, Model

# Define the message model
class Dream(Model):
    description: str

# Create a User Agent
user = Agent(name="User", seed="client_seed", port=8001, endpoint=["http://127.0.0.1:8001/submit"])

@user.on_event("startup")
async def send_dream(ctx: Context):
    dream_text = input("Describe your dream: ")
    print("Sending your dream to Dreamie...")

    # Use Dreamie's actual address from the logs
    dreamie_address = "agent1qtu6wt5jphhmdjau0hdhc002ashzjnueqe89gvvuln8mawm3m0xrwmn9a76"  # Replace this

    success = await ctx.send(dreamie_address, Dream(description=dream_text))
    
    if not success:
        print("❌ Failed to send the dream. Make sure Dreamie is running!")

@user.on_message(model=Dream)
async def receive_interpretation(ctx: Context, sender: str, dream: Dream):
    print(f"\n🌙 Dreamie interprets: {dream.description}")

if __name__ == "__main__":
    user.run()
```

## **Step 4: Running the Agents**

### **1. Start the Dream Agent**

Run the Dream Agent in the **Ubuntu terminal**:

```bash
python dream_agent.py
```

After starting, it will print an **agent address** (e.g., `agent1qtu6wt...`). Copy this address and paste it into **`dream_user.py`** in place of `dreamie_address`.

### **2. Start the User Agent**

Open another terminal, navigate to the `dream` folder, and run:

```bash
python dream_user.py
```

Enter a dream description when prompted, and wait for Dreamie’s interpretation.

## **Expected Output**

1. The **Dream Agent** logs:
   ```
   INFO: [Dreamie]: Hello, I'm Dreamie, your AI Dream Interpreter!
   INFO: [Dreamie]: My address: agent1qtu6wt5jphhmdjau0hdhc002ashzjnueqe89gvvuln8mawm3m0xrwmn9a76
   ```

2. The **User Agent** prompts:
   ```
   Describe your dream: I was flying in the sky
   Sending your dream to Dreamie...
   🌙 Dreamie interprets: Flying in your dream? You crave freedom and adventure! Maybe it's time for a spontaneous trip!
   ```

## **Conclusion**

You have successfully built a **multi-agent AI system** using Fetch.ai's uAgents! 🚀 Your **Dream Agent** and **User Agent** can communicate seamlessly, enabling real-time AI-powered dream interpretations.

Happy coding! 🎭✨
