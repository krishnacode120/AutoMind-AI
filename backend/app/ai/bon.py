"""Core BON orchestrator."""

from app.ai.context_builder import ContextBuilder
from app.ai.conversation_memory import ConversationMemory
from app.ai.intent_parser import IntentParser
from app.ai.knowledge_engine import KnowledgeEngine
from app.ai.response_formatter import ResponseFormatter
from app.ai.types import BONRequest, BONResponse


class BONAssistant:
    """Orchestrates the pipeline components to process user requests."""

    def __init__(self, context_builder: ContextBuilder | None = None) -> None:
        """Initialize the core AI components."""
        self.memory = ConversationMemory()
        self.intent_parser = IntentParser()
        self.context_builder = context_builder or ContextBuilder(memory=self.memory)
        self.knowledge_engine = KnowledgeEngine()
        self.response_formatter = ResponseFormatter()

    def process(self, request: BONRequest) -> BONResponse:
        """Process a request sequentially through the BON pipeline."""

        # 1. Update memory with the user's message
        self.memory.append_message(
            session_id=request.session_id, role="user", content=request.message
        )

        # 2. Parse the intent
        intent_result = self.intent_parser.parse(request.message)

        # 3. Build context
        context = self.context_builder.build(
            vehicle_id=request.vehicle_id,
            intent=intent_result.intent,
            session_id=request.session_id,
        )

        # 4. Generate answer
        answer = self.knowledge_engine.answer(intent_result.intent, context)

        # 5. Format response
        response = self.response_formatter.format(
            answer=answer,
            intent=intent_result.intent,
            confidence=intent_result.confidence,
            context=context.model_dump(mode="json"),
        )

        # 6. Update memory with assistant's response
        self.memory.append_message(
            session_id=request.session_id, role="assistant", content=response.answer
        )

        return response
