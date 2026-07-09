import { useCallback, useEffect, useMemo, useState } from "react";

import {
  sendMessage as sendBONMessage,
  type BONResponse,
} from "../services/bonApi";

const SESSION_STORAGE_KEY = "automind-bon-session-id";
const MESSAGE_STORAGE_PREFIX = "automind-bon-messages";

export type BONMessageRole = "user" | "assistant" | "error";

export type BONChatMessage = {
  id: string;
  role: BONMessageRole;
  content: string;
  timestamp: string;
  intent?: string;
  confidence?: number;
};

type UseBONResult = {
  messages: BONChatMessage[];
  loading: boolean;
  sessionId: string;
  lastFailedMessage: string | null;
  sendMessage: (message: string) => Promise<void>;
  clearConversation: () => void;
  retryLastMessage: () => Promise<void>;
};

function createId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }

  return `${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

function getStoredSessionId(): string {
  const storedSessionId = localStorage.getItem(SESSION_STORAGE_KEY);

  if (storedSessionId) {
    return storedSessionId;
  }

  const sessionId = createId();
  localStorage.setItem(SESSION_STORAGE_KEY, sessionId);
  return sessionId;
}

function getMessageStorageKey(sessionId: string): string {
  return `${MESSAGE_STORAGE_PREFIX}:${sessionId}`;
}

function loadMessages(sessionId: string): BONChatMessage[] {
  const storedMessages = localStorage.getItem(getMessageStorageKey(sessionId));

  if (!storedMessages) {
    return [];
  }

  try {
    return JSON.parse(storedMessages) as BONChatMessage[];
  } catch {
    return [];
  }
}

function createUserMessage(content: string): BONChatMessage {
  return {
    id: createId(),
    role: "user",
    content,
    timestamp: new Date().toISOString(),
  };
}

function createAssistantMessage(response: BONResponse): BONChatMessage {
  return {
    id: createId(),
    role: "assistant",
    content: response.answer,
    timestamp: response.timestamp,
    intent: response.intent,
    confidence: response.confidence,
  };
}

function createErrorMessage(): BONChatMessage {
  return {
    id: createId(),
    role: "error",
    content:
      "BON is having trouble responding right now. Check that the backend is running, then try again.",
    timestamp: new Date().toISOString(),
  };
}

export function useBON(vehicleId: number | null): UseBONResult {
  const [sessionId, setSessionId] = useState(getStoredSessionId);
  const [messages, setMessages] = useState<BONChatMessage[]>(() =>
    loadMessages(getStoredSessionId()),
  );
  const [loading, setLoading] = useState(false);
  const [lastFailedMessage, setLastFailedMessage] = useState<string | null>(
    null,
  );

  const messageStorageKey = useMemo(
    () => getMessageStorageKey(sessionId),
    [sessionId],
  );

  useEffect(() => {
    localStorage.setItem(messageStorageKey, JSON.stringify(messages));
  }, [messageStorageKey, messages]);

  const sendMessage = useCallback(
    async (message: string) => {
      const trimmedMessage = message.trim();

      if (!trimmedMessage || loading || !vehicleId) {
        return;
      }

      setMessages((currentMessages) => [
        ...currentMessages,
        createUserMessage(trimmedMessage),
      ]);
      setLoading(true);
      setLastFailedMessage(null);

      try {
        const response = await sendBONMessage({
          vehicle_id: vehicleId,
          message: trimmedMessage,
          session_id: sessionId,
        });

        setMessages((currentMessages) => [
          ...currentMessages,
          createAssistantMessage(response),
        ]);
      } catch {
        setLastFailedMessage(trimmedMessage);
        setMessages((currentMessages) => [
          ...currentMessages,
          createErrorMessage(),
        ]);
      } finally {
        setLoading(false);
      }
    },
    [loading, sessionId, vehicleId],
  );

  const clearConversation = useCallback(() => {
    localStorage.removeItem(messageStorageKey);

    const nextSessionId = createId();
    localStorage.setItem(SESSION_STORAGE_KEY, nextSessionId);
    setSessionId(nextSessionId);
    setMessages([]);
    setLastFailedMessage(null);
  }, [messageStorageKey]);

  const retryLastMessage = useCallback(async () => {
    if (lastFailedMessage) {
      await sendMessage(lastFailedMessage);
    }
  }, [lastFailedMessage, sendMessage]);

  return {
    messages,
    loading,
    sessionId,
    lastFailedMessage,
    sendMessage,
    clearConversation,
    retryLastMessage,
  };
}
