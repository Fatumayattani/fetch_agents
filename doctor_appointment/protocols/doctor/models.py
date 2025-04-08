from uagents import Model
from datetime import datetime, timedelta
from typing import List

class Doctor(Model):
    name: str  # Name of the doctor
    specializations: List[int]  # List of specializations (e.g., 1 for cardiology, 2 for pediatrics)

class Availability(Model):
    doctor: Doctor  # Link to the Doctor model
    time_start: datetime  # Start of the availability period
    time_end: datetime  # End of the availability period

class SpecializationModel(Model):
    type: int  # Type of specialization (e.g., 1 for cardiology, 2 for pediatrics)
    description: str  # Description of the specialization
