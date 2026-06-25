from app.models.conversation import ConversationContext

class PipelineRouter:
    def route(self, context: ConversationContext):
        # A lightweight router to determine pipeline type.
        # In a real app, this could be an LLM call or regex classifier.
        # For V2.5, we'll keep it simple and default to the search strategy passed by frontend,
        # or determine if RAG/Web is needed based on the context.pipeline_type which might be set 
        # by the frontend. If it's not set, we default to hybrid.
        
        query = context.user_query.lower()
        if "search" in query or "web" in query:
            context.pipeline_type = "web"
        elif "document" in query or "file" in query or "report" in query:
            context.pipeline_type = "rag"
        elif not context.pipeline_type:
            context.pipeline_type = "hybrid" # default to both
