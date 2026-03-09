import asyncio
from database import SessionLocal
from channels.router import MessageRouter

async def test_router():
    db = SessionLocal()
    router = MessageRouter(db)
    
    # Force the condition where lead is "converted"
    import sys
    
    try:
        if router.ai.client:
            print("Try generating content...")
            r = router.ai.answer_followup_question("Testing follow up question")
            print("Response:", r)
        else:
            print("Model is NONE")
    except Exception as e:
        print(f"ERROR CAUGHT: {type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_router())
