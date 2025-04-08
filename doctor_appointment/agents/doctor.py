import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from uagents import Agent, Context
from tortoise import Tortoise
from protocols.doctor import (
    SpecializationModel,
    Doctor,
    Availability,
    AppointmentRequest,
    AppointmentResponse,
    AppointmentConfirmation,
    ConfirmationResponse
)
from datetime import datetime
from pytz import utc

# Define the doctor agent
doctor = Agent(
    name="DrSmith",
    port=8001,
    seed="doctor secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)

# NOTE: Removed doctor.include(doctor_proto) to avoid duplicate model registration

# Initialize the database and populate doctor data on startup
@doctor.on_event("startup")
async def init_db(ctx: Context):
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["protocols.doctor.models"]}
    )
    await Tortoise.generate_schemas()

    # Create doctor and availability
    doc = await Doctor.create(name=doctor.name, location="City Hospital")
    spec = await SpecializationModel.create(type=2)  # Cardiology
    await doc.specializations.add(spec)

    await Availability.create(
        doctor=doc,
        time_start=utc.localize(datetime(2023, 10, 1, 9, 0)),
        time_end=utc.localize(datetime(2023, 10, 1, 17, 0))
    )

# Handle incoming appointment request
@doctor.on_message(model=AppointmentRequest)
async def handle_appointment_request(ctx: Context, sender: str, msg: AppointmentRequest):
    ctx.logger.info(f"Received appointment request from {msg.patient}")

    proposed_time = msg.preferred_time

    response = AppointmentResponse(
        doctor_name=doctor.name,
        proposed_time=proposed_time,
        fee=2000,
        accept=True
    )
    await ctx.send(sender, response)
    ctx.logger.info("Sent appointment response to patient")

# Handle confirmation from patient
@doctor.on_message(model=AppointmentConfirmation)
async def handle_confirmation(ctx: Context, sender: str, msg: AppointmentConfirmation):
    ctx.logger.info(f"Appointment confirmed by {msg.patient_name} at {msg.appointment_time}")

    response = ConfirmationResponse(message="Appointment confirmed. See you soon!")
    await ctx.send(sender, response)
    ctx.logger.info("Sent confirmation response to patient")

# Close DB on shutdown
@doctor.on_event("shutdown")
async def close_db(ctx: Context):
    await Tortoise.close_connections()

if __name__ == "__main__":
    doctor.run()
