# BON Architecture

BON is a deterministic vehicle assistant in the current release. It does not
call a hosted model or require an API key.

1. `IntentParser` categorizes a user message.
2. `ContextBuilder` collects vehicle, latest telemetry, calculated reports, and
   the last ten conversation exchanges.
3. `KnowledgeEngine` produces an intent-specific response from that context.
4. `ResponseFormatter` returns the structured answer to the BON API.

Supported intents include vehicle, telemetry, health, alerts, maintenance,
prediction, general, and unknown. The context builder treats unavailable data
as absent instead of failing the entire conversation.

Ollama settings remain available for a future opt-in language-model adapter;
they are not used by the active assistant flow.
