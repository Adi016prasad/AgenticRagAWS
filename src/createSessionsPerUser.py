import os
import json

app = FastAPI()

@app.post("/createSessionsPerUser")
async def create_sessions_per_user(request: Request):
    data = await request.json()

    userId = data.get("userId", "")
    if userId == "":
        return JSONResponse(content={"error": "userId is required"}, status_code=400)
    
    sessionId = 