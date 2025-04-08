import sys
import os

# Add the parent directory of 'protocols' to sys.path so it can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Now you should be able to import the protocol from the correct path
from protocols.doctor import doctor_proto
from protocols.doctor.messages import AppointmentRequest, AppointmentResponse, AppointmentConfirmation, ConfirmationResponse # type: ignore
from protocols.doctor.models import Doctor, Availability

from uagents import Agent, Context

# Register the protocol
doctor_proto.include()

class DoctorAgent(Agent):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name

    @doctor_proto.on_message(model=AppointmentRequest, replies=AppointmentResponse)
    async def handle_appointment_request(self, ctx: Context, sender: str, msg: AppointmentRequest):
        doctor = await Doctor.filter(name=self.name).first()
        if not doctor:
            await ctx.send(sender, AppointmentResponse(accept=False))
            return

        availability = await Availability.filter(doctor=doctor).first()
        if not availability:
            await ctx.send(sender, AppointmentResponse(accept=False))
            return

        if msg.required_specialization not in [spec.type for spec in await doctor.specializations.all()]:
            await ctx.send(sender, AppointmentResponse(accept=False))
            return

        if (msg.preferred_time >= availability.time_start and
            (msg.preferred_time + msg.duration) <= availability.time_end):
            
            fee = 2000 * (msg.duration.total_seconds() / 3600)
            
            await ctx.send(sender, AppointmentResponse(
                accept=True,
                proposed_time=msg.preferred_time,
                doctor_name=self.name,
                fee=fee
            ))
        else:
            await ctx.send(sender, AppointmentResponse(accept=False))

    @doctor_proto.on_message(model=AppointmentConfirmation, replies=ConfirmationResponse)
    async def handle_appointment_confirmation(self, ctx: Context, sender: str, msg: AppointmentConfirmation):
        doctor = await Doctor.filter(name=msg.doctor_name).first()
        availability = await Availability.filter(doctor=doctor).first()

        if not doctor or not availability:
            await ctx.send(sender, ConfirmationResponse(success=False, message="Doctor or availability not found"))
            return

        if (msg.appointment_time >= availability.time_start and
            (msg.appointment_time + msg.duration) <= availability.time_end):
            availability.time_start = msg.appointment_time + msg.duration
            await availability.save()

            await ctx.send(sender, ConfirmationResponse(success=True, message="Appointment booked successfully"))
        else:
            await ctx.send(sender, ConfirmationResponse(success=False, message="Time unavailable"))

if __name__ == "__main__":
    doctor_agent = DoctorAgent(name="DrSmith")  # The Doctor agent's name
    doctor_agent.run()
