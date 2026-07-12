from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import enum


# ------------------------------------------------------------------
# User Roles
# ------------------------------------------------------------------

class RoleEnum(str, enum.Enum):
    PATIENT = "patient"
    CAREGIVER = "caregiver"
    DOCTOR = "doctor"


# ------------------------------------------------------------------
# Request Models
# ------------------------------------------------------------------

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum

    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    phone: Optional[str] = None

    # Doctor fields
    specialization: Optional[str] = None
    license_number: Optional[str] = Field(
        default=None,
        alias="licenseNumber",
    )

    # Caregiver field
    linked_patient_id: Optional[str] = Field(
        default=None,
        alias="linkedPatientId",
    )

    # Patient field
    patient_id: Optional[str] = Field(
        default=None,
        alias="patientId",
    )

    class Config:
        populate_by_name = True


# ------------------------------------------------------------------
# Response Models
# ------------------------------------------------------------------

class UserResponse(BaseModel):
    id: str

    email: EmailStr
    role: RoleEnum

    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    phone: Optional[str] = None

    specialization: Optional[str] = None

    license_number: Optional[str] = Field(
        default=None,
        alias="licenseNumber",
    )

    linked_patient_id: Optional[str] = Field(
        default=None,
        alias="linkedPatientId",
    )

    patient_id: Optional[str] = Field(
        default=None,
        alias="patientId",
    )

    class Config:
        from_attributes = True
        populate_by_name = True