type EventHandler = (data: any) => void;

export class EventEmitter {
  private listeners: Record<string, EventHandler[]> = {};

  on(event: string, handler: EventHandler) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event].push(handler);
  }

  off(event: string, handler: EventHandler) {
    if (!this.listeners[event]) return;
    this.listeners[event] = this.listeners[event].filter((h) => h !== handler);
  }

  emit(event: string, data?: any) {
    if (!this.listeners[event]) return;
    this.listeners[event].forEach((handler) => handler(data));
  }
}
