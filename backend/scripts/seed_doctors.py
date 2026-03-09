"""Seed script to migrate mock JSON data into the real SQL database."""

import os
import sys
import json
from pathlib import Path

# Add backend directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, engine, Base
from models.hospital import Specialty, Doctor, AppointmentSlot

def seed_database():
    print("Creating tables in SQLite/PostgreSQL...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Load JSON
    file_path = Path(__file__).parent.parent / "mock_data" / "doctors.json"
    with open(file_path, "r") as f:
        data = json.load(f)
        
    print("Seeding database with Hospital Data...")
    for spec_data in data["specialties"]:
        # Find or create Specialty
        spec = db.query(Specialty).filter(Specialty.name == spec_data["name"]).first()
        if not spec:
            spec = Specialty(
                name=spec_data["name"], 
                preparation_instructions=spec_data.get("preparation", "")
            )
            db.add(spec)
            db.commit()
            db.refresh(spec)
        
        for doc_data in spec_data["doctors"]:
            # Find or create Doctor
            doc = db.query(Doctor).filter(Doctor.name == doc_data["name"]).first()
            if not doc:
                doc = Doctor(name=doc_data["name"], specialty_id=spec.id)
                db.add(doc)
                db.commit()
                db.refresh(doc)
                
            for slot_data in doc_data["slots"]:
                # Find or create Slot
                slot = db.query(AppointmentSlot).filter(AppointmentSlot.id == slot_data["id"]).first()
                if not slot:
                    slot = AppointmentSlot(
                        id=slot_data["id"],
                        doctor_id=doc.id,
                        date=slot_data["date"],
                        time=slot_data["time"],
                        is_available=slot_data.get("available", True)
                    )
                    db.add(slot)
    
    db.commit()
    db.close()
    print("✅ Seeding complete! The AI will now pull real availability from the database.")

if __name__ == "__main__":
    seed_database()
