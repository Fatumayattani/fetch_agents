from uagents import Agent, Context
from protocols.doctor import (
    AppointmentRequest,
    AppointmentConfirmation,
    AppointmentResponse,  
    ConfirmationResponse,
)
from datetime import datetime, timedelta
from pytz import utc
from protocols.doctor.models import Specialization


DOCTOR_ADDRESS = "agent1qw04ejpzg8v3pyg9t7hsxryhmt9vruvwndwyzplaag6cpq6hmshg29qr5wr"

patient = Agent(
    name="PatientAlice",
    port=8000,
    seed="patient secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

req = AppointmentRequest(
    patient="PatientAlice",
    preferred_time=utc.localize(datetime(2023, 10, 1, 10, 0)),
    duration=timedelta(hours=1),
    required_specialization=Specialization.CARDIOLOGY.value,
    patient_info="Chest pain",
)

@patient.on_interval(period=5.0)
async def send_request(ctx: Context):
    if not ctx.storage.get("confirmed"):
        await ctx.send(DOCTOR_ADDRESS, req)
        ctx.logger.info("Sent appointment request")

@patient.on_message(model=AppointmentResponse)
async def handle_response(ctx: Context, sender: str, msg: AppointmentResponse):
    if msg.accept:
        confirm = AppointmentConfirmation(
            patient_name=req.patient,
            appointment_time=msg.proposed_time,
            duration=req.duration,
            doctor_name=msg.doctor_name,
            fee=msg.fee
        )
        await ctx.send(sender, confirm)
        ctx.logger.info("Sent appointment confirmation")
    else:
        ctx.logger.info("Appointment request was not accepted")
        ctx.storage.set("confirmed", True)

@patient.on_message(model=ConfirmationResponse)
async def handle_confirm(ctx: Context, _: str, msg: ConfirmationResponse):
    ctx.logger.info(f"Confirmation received: {msg.message}")
    ctx.storage.set("confirmed", True)

if __name__ == "__main__":
    patient.run()
