import httpx
import asyncio
from config import get_settings

async def test():
    s = get_settings()
    url = f"https://graph.facebook.com/v18.0/{s.whatsapp_phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {s.whatsapp_access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": "918270001923",
        "type": "text",
        "text": {"body": "Test message from API"}
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        print(response.status_code, response.text)

asyncio.run(test())
