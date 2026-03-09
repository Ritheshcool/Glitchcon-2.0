"""Hospital data models (Specialty, Doctor, Slots)."""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class Specialty(Base):
    __tablename__ = "specialties"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    preparation_instructions = Column(Text, nullable=True)

    doctors = relationship("Doctor", back_populates="specialty")

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    specialty_id = Column(Integer, ForeignKey("specialties.id"), nullable=False)

    specialty = relationship("Specialty", back_populates="doctors")
    slots = relationship("AppointmentSlot", back_populates="doctor")

class AppointmentSlot(Base):
    __tablename__ = "appointment_slots"

    id = Column(String(50), primary_key=True, index=True) # e.g., ORTH-001
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    date = Column(String(20), nullable=False) # stored as "2026-03-10"
    time = Column(String(20), nullable=False) # stored as "09:00 AM"
    is_available = Column(Boolean, default=True, nullable=False)

    doctor = relationship("Doctor", back_populates="slots")
