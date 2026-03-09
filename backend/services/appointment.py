"""Appointment booking service — check availability and book slots."""

from sqlalchemy.orm import Session
from models.lead import Lead, LeadStatus
from models.appointment import Appointment
from models.conversation import InteractionLog
from models.hospital import Specialty, Doctor, AppointmentSlot


class AppointmentService:
    def __init__(self, db: Session):
        self.db = db

    def check_doctor_availability(self, specialty: str, date_range: list[str] = None) -> list[dict]:
        """
        check_doctor_availability(specialty, date_range) → available slots from database
        """
        query = (
            self.db.query(AppointmentSlot)
            .join(Doctor)
            .join(Specialty)
            .filter(Specialty.name.ilike(f"%{specialty}%"))
            .filter(AppointmentSlot.is_available == True)
        )
        
        if date_range:
            query = query.filter(AppointmentSlot.date.in_(date_range))
            
        slots = query.all()
        
        results = []
        for slot in slots:
            results.append({
                "slot_id": slot.id,
                "doctor_name": slot.doctor.name,
                "specialty": slot.doctor.specialty.name,
                "date": slot.date,
                "time": slot.time,
                "preparation": slot.doctor.specialty.preparation_instructions or "",
            })
        return results

    def book_appointment(self, lead_id: int, slot_id: str) -> dict:
        """
        book_appointment(lead_id, slot_id) → confirms booking + sends confirmation
        """
        lead = self.db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            return {"error": "Lead not found"}

        # Find the slot in database and lock it
        slot = self.db.query(AppointmentSlot).filter(AppointmentSlot.id == slot_id, AppointmentSlot.is_available == True).first()
        
        if not slot:
            return {"error": "Slot not found or already booked"}

        # Mark as unavailable
        slot.is_available = False
        
        # Create appointment
        appointment = Appointment(
            lead_id=lead_id,
            doctor_name=slot.doctor.name,
            specialty=slot.doctor.specialty.name,
            slot_date=slot.date,
            slot_time=slot.time,
            slot_id=slot.id,
            status="confirmed",
            preparation_instructions=slot.doctor.specialty.preparation_instructions or "",
        )
        self.db.add(appointment)

        # Update lead status
        lead.status = LeadStatus.CONVERTED
        self.db.commit()
        self.db.refresh(appointment)

        # Log
        log = InteractionLog(
            lead_id=lead_id,
            stage="booking",
            outcome="confirmed",
            details=f"Booked with {slot.doctor.name} on {slot.date} at {slot.time}",
        )
        self.db.add(log)
        self.db.commit()

        confirmation = {
            "appointment_id": appointment.id,
            "status": "confirmed",
            "doctor": slot.doctor.name,
            "specialty": slot.doctor.specialty.name,
            "date": slot.date,
            "time": slot.time,
            "preparation_instructions": slot.doctor.specialty.preparation_instructions or "",
            "confirmation_message": (
                f"✅ Your appointment is confirmed!\n\n"
                f"👨‍⚕️ Doctor: {slot.doctor.name}\n"
                f"🏥 Department: {slot.doctor.specialty.name}\n"
                f"📅 Date: {slot.date}\n"
                f"⏰ Time: {slot.time}\n\n"
                f"📋 Preparation:\n{slot.doctor.specialty.preparation_instructions or 'None'}\n\n"
                f"We look forward to seeing you!"
            ),
        }
        return confirmation

    def get_all_appointments(self) -> list[dict]:
        """Get all appointments."""
        appointments = self.db.query(Appointment).all()
        return [
            {
                "id": a.id,
                "lead_id": a.lead_id,
                "doctor_name": a.doctor_name,
                "specialty": a.specialty,
                "date": a.slot_date,
                "time": a.slot_time,
                "status": a.status,
            }
            for a in appointments
        ]
