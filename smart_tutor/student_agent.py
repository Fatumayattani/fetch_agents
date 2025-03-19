from uagents import Agent, Context, Model

# Define message models
class Question(Model):
    text: str

class Answer(Model):
    text: str

# Initialize Student Agent
student = Agent(name="Student", seed="student_secret_seed", port=8001, endpoint=["http://127.0.0.1:8001/submit"])

@student.on_event("startup")
async def ask_question(ctx: Context):
    question_text = input("Ask your question: ")
    print("Sending your question to the Tutor...")

    # Use Tutor's actual address (replace with real address from logs)
    tutor_address = "agent1qt024pv43ckcpmvezps0maw7hqaexa5sakw5qh4xgwvwmpm0at0azpmdxqs"  

    success = await ctx.send(tutor_address, Question(text=question_text))
    
    if not success:
        print("❌ Failed to send the question. Make sure Tutor is running!")

@student.on_message(model=Answer)
async def receive_answer(ctx: Context, sender: str, answer: Answer):
    print(f"\n📚 Tutor says: {answer.text}")

if __name__ == "__main__":
    student.run()

