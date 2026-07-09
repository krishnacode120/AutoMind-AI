import { Bot, RotateCw, UserRound } from "lucide-react";

import type { BONChatMessage } from "../../hooks/useBON";

type BONMessageProps = {
  message: BONChatMessage;
  showRetry?: boolean;
  onRetry?: () => void;
};

function BONMessage({ message, showRetry = false, onRetry }: BONMessageProps) {
  const isUser = message.role === "user";
  const isError = message.role === "error";
  const classes = [
    "bon-message",
    isUser ? "bon-message--user" : "bon-message--assistant",
    isError ? "bon-message--error" : "",
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <div className={classes}>
      <div className="bon-message__avatar" aria-hidden="true">
        {isUser ? <UserRound size={18} /> : <Bot size={18} />}
      </div>
      <div className="bon-message__content">
        <p>{message.content}</p>
        {message.intent && (
          <span className="bon-message__meta">
            {message.intent} - {Math.round((message.confidence ?? 0) * 100)}%
          </span>
        )}
        {showRetry && onRetry && (
          <button className="bon-message__retry" type="button" onClick={onRetry}>
            <RotateCw size={14} />
            Retry
          </button>
        )}
      </div>
    </div>
  );
}

export default BONMessage;
