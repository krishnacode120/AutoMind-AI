"""BON assistant API routes."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.ai.bon import BONAssistant
from app.ai.types import BONRequest, BONResponse
from app.database.session import get_db
from app.services.vehicle_service import get_vehicle
from app.utils.helpers import success_response


router = APIRouter(prefix="/bon", tags=["BON"])
_bon_assistant = BONAssistant()


def get_bon_assistant() -> BONAssistant:
    """Return the shared BON assistant instance."""
    return _bon_assistant


@router.post("/chat", response_model=BONResponse)
async def chat(
    request: BONRequest,
    db: Session = Depends(get_db),
    assistant: BONAssistant = Depends(get_bon_assistant),
) -> BONResponse:
    """Process a chat request through BON."""
    try:
        if get_vehicle(db, request.vehicle_id) is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid vehicle",
            )

        return assistant.process(request)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to process BON request",
        ) from exc


@router.get("/sessions/{session_id}")
async def get_session_history(
    session_id: str,
    assistant: BONAssistant = Depends(get_bon_assistant),
) -> dict[str, Any]:
    """Return conversation history for a session."""
    if not _session_exists(assistant, session_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    return success_response(
        message="Conversation history retrieved successfully",
        data={
            "session_id": session_id,
            "history": assistant.memory.get_history(session_id),
        },
    )


@router.delete("/sessions/{session_id}")
async def clear_session_history(
    session_id: str,
    assistant: BONAssistant = Depends(get_bon_assistant),
) -> dict[str, Any]:
    """Clear conversation history for a session."""
    if not _session_exists(assistant, session_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    assistant.memory.clear_session(session_id)
    return success_response(
        message="Conversation history cleared successfully",
        data={"session_id": session_id},
    )


@router.get("/health")
async def bon_health() -> dict[str, str]:
    """Return BON service health."""
    return {
        "service": "BON",
        "status": "online",
        "version": "1.0",
    }


def _session_exists(assistant: BONAssistant, session_id: str) -> bool:
    """Return whether a conversation session exists."""
    sessions = getattr(assistant.memory, "_sessions", {})
    return session_id in sessions
