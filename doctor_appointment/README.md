# 🚑 Doctor Appointment System with uAgents

A decentralized doctor appointment system built using the uAgents framework (Fetch.AI), enabling seamless communication between patient and doctor agents for appointment management.

## Features

- 🩺 **Autonomous Agent Communication**
- 📅 **Appointment Request/Response Protocol**
- ⏰ **Real-time Availability Checking**
- 💼 **Doctor Specialization Matching**
- 💵 **Automated Fee Calculation**
- 🔄 **Dynamic Schedule Updates**
- 📍 **Location-based Service Discovery**
- 📊 **Persistent Storage with SQLite**

## Prerequisites

- Python 3.9+
- Poetry package manager
- Basic understanding of agent-based systems

## Installation

```bash
# Clone repository
git clone https://github.com/Fatumayattani/fetch_agents.git
cd doctor_appointment

# Install dependencies
poetry install

# Initialize database
poetry run python -m tortoise init --config pyproject.toml
```

## Project Structure

```
doctor-appointment/
├── protocols/
│   └── doctor/
│       ├── __init__.py       # Protocol definitions and message handlers
│       └── models.py         # Database models and enums
└── agents/
    ├── doctor.py             # Doctor agent implementation
    └── patient.py            # Patient agent implementation
```

## How to Run

1. **Start Doctor Agent** (in terminal 1):
```bash
poetry run python agents/doctor.py
```

2. **Note Doctor Agent Address** from console output:

INFO: [DrSmith]: Agent address: agent1qdfdx6952trs028fxyug7elgcktam9f896ays6u9art4uaf75hwy2j9m87w


3. **Update Patient Agent**:

# In agents/patient.py
DOCTOR_ADDRESS = "agent1qdfdx6952trs028fxyug7elgcktam9f896ays6u9art4uaf75hwy2j9m87w"


4. **Start Patient Agent** (in terminal 2):
```bash
poetry run python agents/patient.py
```

## Expected Output

**Doctor Agent Logs:**
INFO: [DrSmith]: Received appointment request from PatientAlice
INFO: [DrSmith]: Checking availability for 2023-10-01 10:00:00+00:00
INFO: [DrSmith]: Availability confirmed - sending response
INFO: [DrSmith]: Received booking confirmation - updating schedule


**Patient Agent Logs:**
INFO: [PatientAlice]: Sent appointment request for Cardiology consultation
INFO: [PatientAlice]: Received availability confirmation from DrSmith
INFO: [PatientAlice]: Appointment booked successfully for 2023-10-01 10:00:00+00:00


## Key Components

### Protocol Definitions
- **AppointmentRequest**: Patient-initiated message with time preferences and medical needs
- **AppointmentResponse**: Doctor's availability status and proposed terms
- **AppointmentConfirmation**: Final booking details
- **Specialization Types**: Cardiology, Dermatology, Neurology, General Practice

### Database Models
- `Doctor`: Stores professional details and availability
- `Patient`: Maintains patient records and contact information
- `Availability`: Manages doctor's working hours
- `Specialization`: Defines medical expertise areas

### Agent Features
- **Doctor Agent**:
  - Maintains availability schedule
  - Handles incoming requests
  - Updates availability after bookings
  - Manages specialization offerings

- **Patient Agent**:
  - Initiates appointment requests
  - Negotiates time slots
  - Handles payment calculations
  - Manages booking confirmations

## Technology Stack

- [uAgents Framework](https://fetch.ai/uAgents/) - Agent communication platform
- [Tortoise ORM](https://tortoise-orm.readthedocs.io/) - Database management
- [Pytz](https://pythonhosted.org/pytz/) - Timezone handling
- [Poetry](https://python-poetry.org/) - Dependency management
- [Almanac Contract](https://agentverse.ai/docs) - Agent discovery service

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add new specialization type'`)
4. Push to branch (`git push origin feature/improvement`)
5. Create Pull Request

## License

MIT License - See [LICENSE](LICENSE) for details

---

**Note:** Ensure agents remain online during communication and update doctor addresses when restarting agents. For production use, implement additional security measures and proper error handling.