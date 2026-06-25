from typing import Dict, Any
from app.events.base import BaseEvent
from app.diagnostics.event_bus import event_bus

class DiagnosticsAggregator:
    def __init__(self):
        self.latest_state: Dict[str, Any] = {
            "telemetry": {},
            "pipeline": {},
            "retrieval": {},
            "prompt": {},
            "generation": {}
        }
        event_bus.subscribe(self.handle_event)
        
    def handle_event(self, event: BaseEvent):
        event_dict = event.model_dump()
        event_type = type(event).__name__
        
        if event_type == "PipelineEvent":
            self.latest_state["pipeline"] = event_dict
        elif event_type == "RetrieverEvent":
            self.latest_state["retrieval"] = event_dict
        elif event_type == "PromptEvent":
            self.latest_state["prompt"] = event_dict
        elif event_type == "GenerationEvent":
            self.latest_state["generation"] = event_dict
            
        # Update high-level telemetry
        if "latency_ms" in event_dict and event_dict["latency_ms"] is not None:
            stage_latency_key = f"{event_dict['stage']}_latency_ms"
            self.latest_state["telemetry"][stage_latency_key] = event_dict["latency_ms"]

diagnostics_aggregator = DiagnosticsAggregator()
