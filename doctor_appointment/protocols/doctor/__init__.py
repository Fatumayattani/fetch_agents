from datetime import datetime, timedelta
from typing import Optional
from uagents import Context, Model, Protocol
from pytz import utc
from .models import Doctor, Availability, SpecializationModel

class AppointmentRequest(Model):
    patient: str
    preferred_time: datetime
    duration: timedelta
    required_specialization: int
    patient_info: str

class AppointmentResponse(Model):
    accept: bool
    proposed_time: Optional[datetime] = None
    doctor_name: Optional[str] = None
    fee: Optional[float] = None

class AppointmentConfirmation(Model):
    patient_name: str
    appointment_time: datetime
    duration: timedelta
    doctor_name: str
    fee: float

class ConfirmationResponse(Model):
    success: bool
    message: Optional[str] = None

doctor_proto = Protocol(name="doctor", version="0.1.0")

@doctor_proto.on_message(model=AppointmentRequest, replies=AppointmentResponse)
async def handle_request(ctx: Context, sender: str, msg: AppointmentRequest):
    doctor = await Doctor.filter(name=ctx.agent.name).first()
    availability = await Availability.get(doctor=doctor)
    specs = [int(spec.type) for spec in await doctor.specializations]
    
    if msg.required_specialization not in specs:
        await ctx.send(sender, AppointmentResponse(accept=False))
        return
    
    if (msg.preferred_time >= availability.time_start and
        (msg.preferred_time + msg.duration) <= availability.time_end):
        fee = doctor.consultation_fee * (msg.duration.total_seconds() / 3600)
        await ctx.send(sender, AppointmentResponse(
            accept=True,
            proposed_time=msg.preferred_time,
            doctor_name=doctor.name,
            fee=fee
        ))
    else:
        await ctx.send(sender, AppointmentResponse(accept=False))

@doctor_proto.on_message(model=AppointmentConfirmation, replies=ConfirmationResponse)
async def handle_confirmation(ctx: Context, sender: str, msg: AppointmentConfirmation):
    doctor = await Doctor.filter(name=msg.doctor_name).first()
    availability = await Availability.get(doctor=doctor)
    
    if (msg.appointment_time >= availability.time_start and
        (msg.appointment_time + msg.duration) <= availability.time_end):
        availability.time_start = msg.appointment_time + msg.duration
        await availability.save()
        await ctx.send(sender, ConfirmationResponse(success=True, message="Booked"))
    else:
        await ctx.send(sender, ConfirmationResponse(success=False, message="Unavailable"))