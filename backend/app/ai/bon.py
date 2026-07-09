"""Core BON orchestrator."""

from app.ai.types import BONRequest, BONResponse
from app.ai.intent_parser import IntentParser
from app.ai.context_builder import ContextBuilder
from app.ai.knowledge_engine import KnowledgeEngine
from app.ai.response_formatter import ResponseFormatter
from app.ai.conversation_memory import ConversationMemory


class BONAssistant:
    """Orchestrates the pipeline components to process user requests."""

    def __init__(self) -> None:
        """Initialize the core AI components."""
        self.intent_parser = IntentParser()
        self.context_builder = ContextBuilder()
        self.knowledge_engine = KnowledgeEngine()
        self.response_formatter = ResponseFormatter()
        self.memory = ConversationMemory()

    def process(self, request: BONRequest) -> BONResponse:
        """Process a request sequentially through the BON pipeline."""
        
        # 1. Update memory with the user's message
        self.memory.append_message(
            session_id=request.session_id,
            role="user",
            content=request.message
        )

        # 2. Parse the intent
        intent_result = self.intent_parser.parse(request.message)

        # 3. Build context
        context = self.context_builder.build(request.vehicle_id, intent_result.intent)

        # 4. Generate answer
        answer = self.knowledge_engine.answer(intent_result.intent, context)

        # 5. Format response
        response = self.response_formatter.format(
            answer=answer,
            intent=intent_result.intent,
            confidence=intent_result.confidence,
            context=context
        )

        # 6. Update memory with assistant's response
        self.memory.append_message(
            session_id=request.session_id,
            role="assistant",
            content=response.answer
        )

        return response
