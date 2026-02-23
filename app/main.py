#import dependencies
from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import date
import uuid


#set the api title
app = FastAPI(title = "AI Regulatory Complaint Router", version="0.1.0")

class IntakeRequest(BaseModel):
    source: str = Field(default="email")
    customer_id: str | None = None
    raw_text: str = Field(min_length=20)

# check the health of the site
@app.get("/health")
def health():
    return {"ok": True, "ts": date.utcnow().isoformat() + "Z"}
    
# Submit an intake or complaint
@app.post("/intake")
def intake(req: IntakeRequest):
    case_id = f"CASE-{uuid.uuid4().hex[:10].upper()}"
    return {"case_id": case_id, "status": "RECEIVED"}
