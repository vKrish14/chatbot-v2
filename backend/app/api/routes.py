from fastapi import APIRouter
from pydantic import BaseModel
import time
from app.models.memory import MemoryProcessRequest, MemoryProcessResponse
from app.memory.manager import memory_manager
from app.models.prompt import PromptImproveRequest, PromptImproveResponse
from app.services.improver import prompt_improver
from app.models.chat import ChatRequest, ChatResponse
from app.services.chat import chat_service

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    timestamp: float

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=time.time()
    )

@router.post("/memory/process", response_model=MemoryProcessResponse)
async def process_memory(request: MemoryProcessRequest):
    processed, stats = memory_manager.process_memory(request.messages, request.context_window)
    return MemoryProcessResponse(
        processed_messages=processed,
        stats=stats
    )

@router.post("/improve-prompt", response_model=PromptImproveResponse)
async def improve_prompt(request: PromptImproveRequest):
    return await prompt_improver.improve_prompt(request.original_prompt)

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    return await chat_service.generate_response(request.messages, request.model)
