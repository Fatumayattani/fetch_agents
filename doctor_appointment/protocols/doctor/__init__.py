# protocols/doctor/__init__.py

from uagents import Protocol

# Define the protocol object for the doctor
doctor_proto = Protocol(name="doctor", version="0.1.0")

# Import message models
from .messages import AppointmentRequest, AppointmentResponse, AppointmentConfirmation, ConfirmationResponse
from .models import Doctor, Availability

# Include the protocol to ensure it's registered with the uagents framework
doctor_proto.include()
