from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from typing import List, Dict
from datetime import datetime, timedelta
from protocols.appointments import (
    AppointmentRequest,
    AppointmentResponse,
    AppointmentConfirmation
)

# Define data models
class AppointmentRequest(Model):
    patient_id: str
    patient_name: str
    requested_time: datetime  
    specialization: str  # e.g., "Cardiology", "Dermatology"

class AppointmentResponse(Model):
    doctor_id: str
    available: bool
    proposed_time: datetime = None
    consultation_fee: float = None

class AppointmentConfirmation(Model):
    patient_id: str
    confirmation: bool

# Initialize AgentMD
AgentMD = Agent(
    name="AgentMD_DrSmith",
    seed="doctor_secret_phrase_123",
    endpoint=["http://localhost:8000"],
    port=8000,
)

fund_agent_if_low(AgentMD.wallet.address())

# Doctor's availability setup
AgentMD._storage = {
    "availability": {
        "slots": [
            datetime.now(pytz.utc) + timedelta(hours=i) 
            for i in range(1, 5)  # 4 available slots
        ],
        "specialization": "Cardiology",
        "fee_per_hour": 150.00
    }
}

@AgentMD.on_message(AppointmentRequest)
async def handle_appointment_request(ctx: Context, sender: str, msg: AppointmentRequest):
    # Check specialization match
    if msg.specialization != ctx.storage.get("specialization"):
        await ctx.send(sender, AppointmentResponse(
            doctor_id=ctx.name,
            available=False,
            proposed_time=None
        ))
        return

    # Find first available slot within requested time ±1 hour
    best_slot = None
    for slot in ctx.storage["availability"]["slots"]:
        if abs((slot - msg.requested_time).total_seconds()) <= 3600:
            best_slot = slot
            break

    if best_slot:
        fee = ctx.storage["fee_per_hour"]
        ctx.logger.info(f"Proposing slot: {best_slot}")
        
        await ctx.send(sender, AppointmentResponse(
            doctor_id=ctx.name,
            available=True,
            proposed_time=best_slot,
            consultation_fee=fee
        ))
    else:
        await ctx.send(sender, AppointmentResponse(
            doctor_id=ctx.name,
            available=False
        ))

@AgentMD.on_message(AppointmentConfirmation)
async def handle_confirmation(ctx: Context, sender: str, msg: AppointmentConfirmation):
    if msg.confirmation:
        ctx.logger.info(f"Appointment confirmed with {sender}")
        # Remove slot from availability
        ctx.storage["availability"]["slots"] = [
            slot for slot in ctx.storage["availability"]["slots"]
            if slot != msg.proposed_time
        ]
    else:
        ctx.logger.info(f"Patient {sender} declined the slot")

if __name__ == "__main__":
    AgentMD.run()