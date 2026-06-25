from fastapi import APIRouter
from app.diagnostics.aggregator import diagnostics_aggregator

router = APIRouter()

@router.get("/diagnostics/state")
async def get_diagnostics_state():
    return diagnostics_aggregator.latest_state
