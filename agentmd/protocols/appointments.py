from uagents import Model
from datetime import datetime
from pydantic import Field

class AppointmentRequest(Model):
    patient_id: str = Field(description="Patient's unique ID")
    patient_name: str = Field(description="Patient's full name")
    requested_time: datetime = Field(description="Preferred appointment time")
    specialization: str = Field(description="Required medical specialization")

class AppointmentResponse(Model):
    doctor_id: str = Field(description="Doctor's unique ID")
    available: bool = Field(description="Availability status")
    proposed_time: datetime | None = Field(default=None, description="Alternative time suggestion")
    consultation_fee: float | None = Field(default=None, description="Calculated consultation fee")

class AppointmentConfirmation(Model):
    patient_id: str = Field(description="Patient's unique ID")
    confirmation: bool = Field(description="Confirmation status")
    proposed_time: datetime | None = Field(default=None, description="Confirmed time slot")