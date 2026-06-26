from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.chat import ChatRequest
from app.models.conversation import ConversationContext
from app.services.router import PipelineRouter
from app.services.context_providers import ContextProvidersLayer
from app.services.prompt_builder import PromptBuilder
from app.services.chat_service import ChatService
from app.events.types import PipelineEvent
from app.diagnostics.event_bus import event_bus
import time

router = APIRouter()
pipeline_router = PipelineRouter()
context_providers = ContextProvidersLayer()
prompt_builder = PromptBuilder()
chat_service = ChatService()

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    start_time = time.time()
    
    # 1. Initialize Conversation Context
    context = ConversationContext(
        session_id=request.session_id,
        user_query=request.messages[-1].content if request.messages else "",
        history=request.messages[:-1] if len(request.messages) > 1 else [],
        model=request.model,
        # Strategy settings would typically come from the frontend via the request
        search_strategy=getattr(request, 'search_strategy', 'similarity'),
        top_k=getattr(request, 'top_k', 4),
        similarity_threshold=getattr(request, 'similarity_threshold', 0.5)
    )
    
    # 2. Route
    pipeline_router.route(context)
    
    # Emit Pipeline Event
    event_bus.emit(PipelineEvent(
        session_id=context.session_id,
        stage="routing",
        query=context.user_query,
        pipeline_type=context.pipeline_type
    ))
    
    # 3. Context Providers Layer (RAG / Web)
    context_providers.populate_context(context)
    
    # 4. Prompt Builder
    prompt_builder.build(context)
    
    # 5. LLM Generation
    # We return the StreamingResponse, the latency for the whole pipeline can only be 
    # fully measured when generation ends, which chat_service handles partially.
    
    return StreamingResponse(
        chat_service.generate_stream(context),
        media_type="text/event-stream"
    )
