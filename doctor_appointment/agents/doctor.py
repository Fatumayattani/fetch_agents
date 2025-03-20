from uagents import Agent, Context
from tortoise import Tortoise
from protocols.doctor import doctor_proto, SpecializationModel, Doctor, Availability
from datetime import datetime
from pytz import utc

doctor = Agent(
    name="DrSmith",
    port=8001,
    seed="doctor secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)

doctor.include(doctor_proto)

@doctor.on_event("startup")
async def init_db(ctx: Context):
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["protocols.doctor.models"]}
    )
    await Tortoise.generate_schemas()
    
    doc = await Doctor.create(name=doctor.name, location="City Hospital")
    spec = await SpecializationModel.create(type=2)  # Cardiology
    await doc.specializations.add(spec)
    
    await Availability.create(
        doctor=doc,
        time_start=utc.localize(datetime(2023, 10, 1, 9, 0)),
        time_end=utc.localize(datetime(2023, 10, 1, 17, 0))
    )

@doctor.on_event("shutdown")
async def close_db(ctx: Context):
    await Tortoise.close_connections()

if __name__ == "__main__":
    doctor.run()