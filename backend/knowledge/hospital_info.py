"""
Hospital Knowledge Base
This module acts as the "brain" or context window for the AI Agent.
It provides precise factual information about the hospital so the AI does not hallucinate.
"""

# Core Hospital Identity
HOSPITAL_NAME = "HealthFirst Multispecialty Hospital"
HOSPITAL_ADDRESS = "123 Healthcare Avenue, Tech Park District, Bengaluru, Karnataka 560100"
HOSPITAL_PHONE = "+91 8000 123 456"
HOSPITAL_EMAIL = "contact@healthfirst.in"
EMERGENCY_NUMBER = "1066"

# General Rules the AI must follow
AI_BEHAVIOR_RULES = """
- You are a helpful triage and booking assistant for HealthFirst Hospital.
- NEVER invent prices, doctors, or treatments not listed in your knowledge.
- If a patient has a life-threatening emergency, immediately tell them to call 1066 or visit the nearest ER. Do NOT try to book an appointment.
- Keep responses concise (under 2 sentences when possible) and professional.
- Use emojis sparingly but warmly.
"""

# Supported Insurances
ACCEPTED_INSURANCE = [
    "Star Health",
    "HDFC ERGO",
    "ICICI Lombard",
    "Niva Bupa",
    "CGHS (Central Government Health Scheme)",
    "Aditya Birla Health"
]

# FAQs to inject into context
FAQS = """
Q: What are the visiting hours?
A: General Ward: 4:00 PM to 7:00 PM. ICU: 11:00 AM to 12:00 PM and 5:00 PM to 6:00 PM.

Q: Is parking available?
A: Yes, we have a 24/7 underground parking facility. Valet service is available at the main entrance.

Q: Do you offer online/video consultations?
A: Yes, tele-consultations are available for Dermatology, Psychiatry, and General Medicine.

Q: Do you have a pharmacy on-site?
A: Yes, our pharmacy is open 24/7 and is located on the ground floor next to the Emergency entrance.

Q: How much does a general consultation cost?
A: General physician consultation is ₹600. Specialist consultations depend on the doctor but generally range from ₹800 to ₹1500.
"""

def get_full_context() -> str:
    """Returns the compiled knowledge base as a system prompt string."""
    return f"""
[HOSPITAL KNOWLEDGE BASE]
Name: {HOSPITAL_NAME}
Address: {HOSPITAL_ADDRESS}
Emergency Contact: {EMERGENCY_NUMBER}

ACCEPTED INSURANCE: {', '.join(ACCEPTED_INSURANCE)}

FREQUENTLY ASKED QUESTIONS:
{FAQS}

CRITICAL RULES FOR YOU (THE AI):
{AI_BEHAVIOR_RULES}
[/END PORTAL KNOWLEDGE]
"""
