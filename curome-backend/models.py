from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, DateTime
from database import Base
import enum
import uuid
from datetime import datetime

class RoleEnum(str, enum.Enum):
    PATIENT = "patient"
    CAREGIVER = "caregiver"
    DOCTOR = "doctor"

class SlotStatusEnum(str, enum.Enum):
    AVAILABLE = "available"
    PENDING_DOCTOR = "pendingDoctor"
    PENDING_CAREGIVER = "pendingCaregiver"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    # Doctor Specific
    specialization = Column(String, nullable=True)
    license_number = Column(String, nullable=True)

    # Patient Specific (e.g. PAT-123456)
    patient_id = Column(String, unique=True, index=True, nullable=True) 

    # Caregiver Specific
    linked_patient_id = Column(String, nullable=True)

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    doctor_id = Column(String, ForeignKey("users.id"), nullable=False)
    patient_id = Column(String, ForeignKey("users.patient_id"), nullable=True)
    caregiver_id = Column(String, ForeignKey("users.id"), nullable=True)
    
    title = Column(String, nullable=True)
    date = Column(String, nullable=False) 
    time = Column(String, nullable=False) 
    duration = Column(Integer, default=30)
    
    status = Column(Enum(SlotStatusEnum), default=SlotStatusEnum.AVAILABLE)
    approval_note = Column(String, nullable=True)
    cancel_reason = Column(String, nullable=True)