from datetime import datetime, timedelta
from uagents import Agent, Context
from protocols.doctor import doctor_proto  # Make sure doctor_proto is imported
from protocols.doctor.messages import AppointmentRequest, AppointmentResponse, AppointmentConfirmation, ConfirmationResponse # type: ignore

# Make sure the protocol is included
doctor_proto.include()  # Register the protocol

class PatientAgent(Agent):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name

    async def send_appointment_request(self, doctor_name: str, preferred_time: datetime, duration: timedelta, specialization: int):
        request = AppointmentRequest(
            patient=self.name,
            preferred_time=preferred_time,
            duration=duration,
            required_specialization=specialization,
            patient_info="General info about the patient"
        )
        await self.send(doctor_name, request)

    @doctor_proto.on_message(model=AppointmentResponse, replies=AppointmentConfirmation)
    async def handle_appointment_response(self, ctx: Context, sender: str, msg: AppointmentResponse):
        if msg.accept:
            print(f"Doctor {msg.doctor_name} accepted the appointment!")
            # Send confirmation back to doctor
            confirmation = AppointmentConfirmation(
                patient_name=self.name,
                appointment_time=msg.proposed_time,
                duration=timedelta(hours=1),  # Example duration
                doctor_name=msg.doctor_name,
                fee=msg.fee
            )
            await self.send(sender, confirmation)
        else:
            print("Doctor rejected the appointment!")

    @doctor_proto.on_message(model=ConfirmationResponse, replies=None)
    async def handle_confirmation_response(self, ctx: Context, sender: str, msg: ConfirmationResponse):
        if msg.success:
            print(f"Appointment confirmed! Doctor: {sender}, Message: {msg.message}")
        else:
            print(f"Appointment failed. Reason: {msg.message}")

if __name__ == "__main__":
    patient_agent = PatientAgent(name="JohnDoe")  # The Patient agent's name
    patient_agent.run()
