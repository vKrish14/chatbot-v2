from typing import List, Callable
from app.events.base import BaseEvent

class EventBus:
    def __init__(self):
        self.subscribers: List[Callable[[BaseEvent], None]] = []
        
    def subscribe(self, callback: Callable[[BaseEvent], None]):
        self.subscribers.append(callback)
        
    def emit(self, event: BaseEvent):
        for subscriber in self.subscribers:
            try:
                subscriber(event)
            except Exception as e:
                print(f"Error in subscriber: {e}")

# Global event bus
event_bus = EventBus()
