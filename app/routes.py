from fastapi import APIRouter, Body
from pydantic import BaseModel
from .service.query import query_thread , query_message , get_doctor_info , get_practice_detail
from .service.message_drafting import draft_message_service
from fastapi import HTTPException
router = APIRouter()

class DraftMessageRequest(BaseModel):
    doctor_id: int
    practice_id: int
    session_id: int
    job_description: str
    pricing: float
    start_time: str
    end_time: str
    date: str
    practice_name: str
    practice_postcode: str

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/ip")
async def get_railway_ip():
    """
    Get Railway's outbound IP address for DigitalOcean whitelisting.
    Use this to find your Railway IP, then add it to DigitalOcean MongoDB trusted sources.
    """
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.ipify.org?format=json")
            ip_data = response.json()
            return {
                "railway_outbound_ip": ip_data["ip"],
                "message": "Add this IP to DigitalOcean MongoDB Trusted Sources",
                "instructions": "Go to DigitalOcean → MongoDB → Settings → Trusted Sources → Add this IP"
            }
    except Exception as e:
        return {"error": str(e), "message": "Could not fetch IP"}

@router.get("/thread/{practice_id}/{doctor_id}")
async def get_thread(practice_id: str, doctor_id: str):
    try:
        return await query_thread(practice_id, doctor_id)
    except HTTPException as e:
        raise e

@router.get("/message/{practice_id}/{doctor_id}")
async def get_message(practice_id: int, doctor_id: int):
    try:
        return await query_message(practice_id, doctor_id)
    except HTTPException as e:
        raise e

@router.get("/doctor/{doctor_id}")
async def fetch_doctor_info(doctor_id: int):
    try:
        return await get_doctor_info(doctor_id)
    except HTTPException as e:
        raise e

@router.get("/practice/{practice_id}")
async def fetch_practice_detail(practice_id: int):
    try:
        return await get_practice_detail(practice_id)
    except HTTPException as e:
        raise e

@router.post("/draft-message")
async def draft_message(request: DraftMessageRequest):
    """
    Draft a message on behalf of a doctor to a practice.
    Uses LangChain agent with Cerebras/Gemini to analyze history and generate message.
    """
    try:
        result = await draft_message_service(
            doctor_id=request.doctor_id,
            practice_id=request.practice_id,
            session_id=request.session_id,
            job_description=request.job_description,
            pricing=request.pricing,
            start_time=request.start_time,
            end_time=request.end_time,
            date=request.date,
            practice_name=request.practice_name,
            practice_postcode=request.practice_postcode
        )
        return result
    except HTTPException as e:
        raise e 