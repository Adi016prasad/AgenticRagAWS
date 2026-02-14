import os
import json
import uuid
from classes import CreateSession
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import Field, BaseModel
import asyncio

if not firebase_admin._apps:
    cred = credentials.Certificate("/home/ubuntu/rag/backend/credentials/college-8c4f8-firebase-adminsdk-fbsvc-9c64238297.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
app = FastAPI()

async def createDocumentSession(sessionId: str, userId: str):
    loop = asyncio.get_event_loop()
    def sync_db_call():
        doc_ref = db.collection("sessions").document(sessionId)
        doc_ref.set({
            "userId": userId,
            "createdAt": firestore.SERVER_TIMESTAMP,
            "status": "active"
        })
    
    await loop.run_in_executor(None, sync_db_call)

@app.post("/createSessionsPerUser")
async def create_sessions_per_user(request: CreateSession):
    userId = ""
    if request.userId:
        userId = request.userId
    
    if userId == "":
        return JSONResponse(content={"error": "userId is required"}, status_code=400)
    
    sessionId  = userId + "-" + str(uuid.uuid4())

    await createDocumentSession(sessionId, userId)
    return {
        "sessionId": sessionId
    }

if "__main__" == __name__:
    uvicorn.run("createSessionsPerUser:app", host = "0.0.0.0", port = 8000, reload = True)