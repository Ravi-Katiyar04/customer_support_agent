# backend/main.py - FastAPI server exposing a simple message endpoint
import os
from dotenv import load_dotenv
from fastapi import FastAPI

# Load .env
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY is missing! Set it in .env or Docker Compose.")
print("✅ GOOGLE_API_KEY loaded successfully")

from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.errors.already_exists_error import AlreadyExistsError

# IMPORTANT: import your app from your local file, not ADK default internal agents
from agents import support_app


  
app = FastAPI(title="ESA Support Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # or "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],   # <-- THIS FIXES THE OPTIONS 405 ERROR
    allow_headers=["*"],
)

# ---------------- SESSION DATABASE ----------------
DB_PATH = os.path.abspath("esa_sessions.db")

# FIX FOR WINDOWS SQLITE PATH
DB_PATH = DB_PATH.replace("\\", "/")

DB_URL = f"sqlite+aiosqlite:///{DB_PATH}"

session_service = DatabaseSessionService(db_url=DB_URL)

# ---------------- ADK RUNNER ----------------
runner = Runner(
    app=support_app,
    session_service=session_service
)

# ---------------- Pydantic Model ----------------
class Message(BaseModel):
    session_id: str
    text: str
    user_id: str = "demo_user"


# ---------------- MESSAGE ENDPOINT ----------------
@app.post("/message")
async def post_message(msg: Message):
    # Create session if does not exist
    try:
        await session_service.create_session(
            app_name=support_app.name,
            user_id=msg.user_id,
            session_id=msg.session_id
    )
    except AlreadyExistsError:
        # Session exists already — safe to continue
        pass


    # Wrap user message as Content
    user_content = types.Content(
        role="user",
        parts=[types.Part(text=msg.text)]
    )

    events = []
    async for event in runner.run_async(
        user_id=msg.user_id,
        session_id=msg.session_id,
        new_message=user_content
    ):
        events.append(event)

    responses = []
    approvals = []

    # Process events
    for e in events:
        if e.content and e.content.parts:
            for p in e.content.parts:

                # Normal text output
                if getattr(p, "text", None):
                    responses.append(p.text)

                # Refund approval workflow
                if getattr(p, "function_call", None):
                    fc = p.function_call
                    if fc.name == "adk_request_confirmation":
                        approvals.append({
                            "approval_id": fc.id,
                            "invocation_id": e.invocation_id,
                            "payload": fc.args
                        })

    return {
        "events": len(events),
        "responses": responses,
        "approvals": approvals
    }


# ---------------- APPROVAL ENDPOINT ----------------
@app.post("/approve")
async def approve(
    invocation_id: str,
    approval_id: str,
    confirmed: bool = True,
    user_id: str = "demo_user",
    session_id: str = "demo_session"
):
    # Create FunctionResponse
    confirmation_response = types.FunctionResponse(
        id=approval_id,
        name="adk_request_confirmation",
        response={"confirmed": confirmed},
    )

    content = types.Content(
        role="user",
        parts=[types.Part(function_response=confirmation_response)]
    )

    events = []
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
        invocation_id=invocation_id
    ):
        events.append(event)

    final_responses = []
    for e in events:
        if e.content and e.content.parts:
            for p in e.content.parts:
                if getattr(p, "text", None):
                    final_responses.append(p.text)

    return {
        "events": len(events),
        "responses": final_responses
    }
