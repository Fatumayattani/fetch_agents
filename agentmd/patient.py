# agents/patient.py
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from datetime import datetime, timedelta

from protocols.appointments import (
    AppointmentRequest,
    AppointmentResponse,
    AppointmentConfirmation
)

# Initialize Patient Agent
PatientAlice = Agent(
    name="PatientAlice",
    seed="patient_secret_phrase_456",
    endpoint=["http://localhost:8001"],
    port=8001,
)

fund_agent_if_low(PatientAlice.wallet.address())

DOCTOR_ADDRESS = "agent1qdfdx6952trs028fxyug7elgcktam9f896ays6u9art4uaf75hwy2j9m87w"

@PatientAlice.on_interval(period=10.0)
async def request_appointment(ctx: Context):
    # Create appointment request
    request = AppointmentRequest(
        patient_id=ctx.name,
        patient_name="Alice Johnson",
        requested_time=datetime.now(pytz.utc) + timedelta(hours=2),
        specialization="Cardiology"
    )
    
    ctx.logger.info("Sending appointment request to AgentMD...")
    await ctx.send(DOCTOR_ADDRESS, request)

@PatientAlice.on_message(AppointmentResponse)
async def handle_response(ctx: Context, sender: str, msg: AppointmentResponse):
    if msg.available:
        ctx.logger.info(f"Received available slot at {msg.proposed_time} (Fee: ${msg.consultation_fee})")
        
        # For simplicity, auto-confirm first available slot
        confirmation = AppointmentConfirmation(
            patient_id=ctx.name,
            confirmation=True,
            proposed_time=msg.proposed_time
        )
        
        await ctx.send(sender, confirmation)
        ctx.logger.info("Appointment confirmed!")
    else:
        ctx.logger.info("No available slots matching criteria")

if __name__ == "__main__":
    PatientAlice.run()