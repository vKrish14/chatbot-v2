from app.models.memory import Message, MemoryStats
from typing import List

class MemoryManager:
    def __init__(self):
        pass
        
    def estimate_tokens(self, text: str) -> int:
        # Rough estimation: 1 token ~= 4 chars in English
        return len(text) // 4
        
    def process_memory(self, messages: List[Message], context_window: int) -> tuple[List[Message], MemoryStats]:
        total_messages = len(messages)
        
        # Keep the last 'context_window' messages
        if total_messages > context_window:
            processed = messages[-context_window:]
        else:
            processed = messages
            
        retained = len(processed)
        tokens = sum(self.estimate_tokens(m.content) for m in processed)
        
        stats = MemoryStats(
            total_messages=total_messages,
            context_window=context_window,
            retained_messages=retained,
            estimated_tokens=tokens
        )
        
        return processed, stats

memory_manager = MemoryManager()
