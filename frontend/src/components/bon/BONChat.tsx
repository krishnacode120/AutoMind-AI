import { Bot, Trash2 } from "lucide-react";
import { useEffect, useRef } from "react";

import { useBON } from "../../hooks/useBON";
import Card from "../common/Card";
import BONInput from "./BONInput";
import BONMessage from "./BONMessage";
import BONSuggestions from "./BONSuggestions";
import BONTyping from "./BONTyping";

type BONChatProps = {
  vehicleId: number;
};

function BONChat({ vehicleId }: BONChatProps) {
  const {
    messages,
    loading,
    lastFailedMessage,
    sendMessage,
    clearConversation,
    retryLastMessage,
  } = useBON(vehicleId);
  const endRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [loading, messages]);

  return (
    <Card className="dashboard-card bon-chat">
      <div className="dashboard-card__header">
        <div>
          <h2 className="dashboard-card__title">Ask BON</h2>
          <p className="bon-chat__subtitle">
            Vehicle assistant for health, alerts, maintenance, and telemetry.
          </p>
        </div>
        <div className="bon-chat__actions">
          <button
            aria-label="Clear conversation"
            className="bon-chat__clear"
            disabled={loading || messages.length === 0}
            type="button"
            onClick={clearConversation}
          >
            <Trash2 size={16} />
          </button>
          <div className="dashboard-card__icon dashboard-card__icon--primary">
            <Bot size={20} />
          </div>
        </div>
      </div>

      <div className="bon-chat__conversation" role="log" aria-live="polite">
        {messages.length === 0 && (
          <div className="bon-chat__empty">
            <Bot size={24} />
            <p>Ask BON a question to start a vehicle-focused conversation.</p>
          </div>
        )}

        {messages.map((message) => (
          <BONMessage
            key={message.id}
            message={message}
            showRetry={
              message.role === "error" &&
              !!lastFailedMessage &&
              message.id === messages[messages.length - 1]?.id
            }
            onRetry={retryLastMessage}
          />
        ))}

        {loading && <BONTyping />}
        <div ref={endRef} />
      </div>

      <BONSuggestions disabled={loading} onSelect={sendMessage} />
      <BONInput disabled={loading} onSend={sendMessage} />
    </Card>
  );
}

export default BONChat;
