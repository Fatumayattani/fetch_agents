from enum import IntEnum
from tortoise import fields, models

class Specialization(IntEnum):
    GENERAL = 1
    CARDIOLOGY = 2
    DERMATOLOGY = 3
    NEUROLOGY = 4

class Patient(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    address = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)

class SpecializationModel(models.Model):
    id = fields.IntField(pk=True)
    type = fields.IntEnumField(Specialization)

class Doctor(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    location = fields.CharField(max_length=64)
    created_at = fields.DatetimeField(auto_now_add=True)
    availability = fields.ReverseRelation["Availability"]
    specializations = fields.ManyToManyField("models.SpecializationModel")
    consultation_fee = fields.FloatField(default=100.0)

class Availability(models.Model):
    id = fields.IntField(pk=True)
    doctor = fields.OneToOneField("models.Doctor", related_name="availability")
    time_start = fields.DatetimeField()
    time_end = fields.DatetimeField()