import { useEffect, useRef, useState } from "react";
import {
  clearSession,
  sendMessage as sendBONMessage,
} from "../services/bonApi";

export type BONMessageRole = "user" | "assistant" | "error";
export type BONChatMessage = {
  id: string;
  role: BONMessageRole;
  content: string;
  timestamp: string;
  intent?: string;
  confidence?: number;
};

function createId(): string {
  return (
    globalThis.crypto?.randomUUID?.() ??
    `${Date.now()}-${Math.random().toString(36).slice(2)}`
  );
}

function storedSession(vehicleId: number | null): string {
  const key = `automind-bon-session:${vehicleId}`;
  try {
    const stored = localStorage.getItem(key);
    if (stored) return stored;
    const id = createId();
    localStorage.setItem(key, id);
    return id;
  } catch {
    return createId();
  }
}

function loadMessages(session: string): BONChatMessage[] {
  try {
    const messages: unknown = JSON.parse(
      localStorage.getItem(`automind-bon-messages:${session}`) ?? "[]",
    );
    return Array.isArray(messages)
      ? messages.filter(
          (item) =>
            item &&
            typeof item.id === "string" &&
            typeof item.content === "string" &&
            typeof item.timestamp === "string" &&
            ["user", "assistant", "error"].includes(item.role),
        )
      : [];
  } catch {
    return [];
  }
}

export function useBON(vehicleId: number | null) {
  const [sessionId, setSessionId] = useState(() => storedSession(vehicleId));
  const [messages, setMessages] = useState(() => loadMessages(sessionId));
  const [loading, setLoading] = useState(false);
  const [lastFailedMessage, setLastFailedMessage] = useState<string | null>(
    null,
  );
  const busy = useRef(false);
  const pending = useRef<AbortController | null>(null);
  useEffect(() => () => pending.current?.abort(), []);
  useEffect(() => {
    try {
      localStorage.setItem(
        `automind-bon-messages:${sessionId}`,
        JSON.stringify(messages.slice(-200)),
      );
    } catch {
      /* Chat still works when local storage is unavailable. */
    }
  }, [messages, sessionId]);

  async function sendMessage(message: string, retry = false): Promise<void> {
    const content = message.trim();
    if (!content || busy.current || !vehicleId) return;
    busy.current = true;
    setLoading(true);
    setLastFailedMessage(null);
    const controller = new AbortController();
    pending.current = controller;
    setMessages((current) =>
      retry
        ? current.filter((item) => item.role !== "error")
        : [
            ...current,
            {
              id: createId(),
              role: "user",
              content,
              timestamp: new Date().toISOString(),
            },
          ],
    );
    try {
      const response = await sendBONMessage(
        { vehicle_id: vehicleId, message: content, session_id: sessionId },
        controller.signal,
      );
      setMessages((current) => [
        ...current,
        {
          id: createId(),
          role: "assistant",
          content: response.answer,
          timestamp: response.timestamp,
          intent: response.intent,
          confidence: response.confidence,
        },
      ]);
    } catch {
      if (!controller.signal.aborted) {
        setLastFailedMessage(content);
        setMessages((current) => [
          ...current,
          {
            id: createId(),
            role: "error",
            content: "BON could not respond. Please try again.",
            timestamp: new Date().toISOString(),
          },
        ]);
      }
    } finally {
      busy.current = false;
      setLoading(false);
    }
  }

  async function clearConversation(): Promise<void> {
    if (busy.current) return;
    busy.current = true;
    setLoading(true);
    try {
      await clearSession(sessionId);
      const next = createId();
      try {
        localStorage.removeItem(`automind-bon-messages:${sessionId}`);
        localStorage.setItem(`automind-bon-session:${vehicleId}`, next);
      } catch {
        /* Storage is optional. */
      }
      setSessionId(next);
      setMessages([]);
      setLastFailedMessage(null);
    } catch {
      setMessages((current) => [
        ...current,
        {
          id: createId(),
          role: "error",
          content: "Conversation could not be cleared. Please try again.",
          timestamp: new Date().toISOString(),
        },
      ]);
    } finally {
      busy.current = false;
      setLoading(false);
    }
  }

  async function retryLastMessage(): Promise<void> {
    if (lastFailedMessage) await sendMessage(lastFailedMessage, true);
  }
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
