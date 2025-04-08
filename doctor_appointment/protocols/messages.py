from uagents import Model
from typing import Optional
from datetime import datetime

class AppointmentRequest(Model):
    patient: str
    preferred_time: datetime

class AppointmentResponse(Model):
    doctor_name: str
    proposed_time: datetime
    fee: int
    accept: bool

class AppointmentConfirmation(Model):
    patient_name: str
    appointment_time: datetime

class ConfirmationResponse(Model):
    message: str
