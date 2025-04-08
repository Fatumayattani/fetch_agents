from uagents import Model
from typing import Optional
from datetime import datetime, timedelta

class AppointmentRequest(Model):
    patient: str  # Name of the patient
    preferred_time: datetime  # Preferred appointment time
    duration: timedelta  # Duration of the appointment
    required_specialization: int  # Specialization required
    patient_info: str  # Additional information about the patient

class AppointmentResponse(Model):
    accept: bool  # Whether the appointment is accepted
    proposed_time: Optional[datetime] = None  # Proposed time for the appointment
    doctor_name: Optional[str] = None  # Name of the doctor proposing the time
    fee: Optional[float] = None  # Consultation fee

class AppointmentConfirmation(Model):
    patient_name: str  # Name of the patient
    appointment_time: datetime  # Confirmed appointment time
    duration: timedelta  # Duration of the appointment
    doctor_name: str  # Name of the doctor confirming the appointment
    fee: float  # Consultation fee

class ConfirmationResponse(Model):
    success: bool  # Whether the appointment was successfully confirmed
    message: Optional[str] = None  # Additional confirmation message
