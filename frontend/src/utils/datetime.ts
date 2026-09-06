/** SQLite's historical timestamps are UTC even when they omit the zone. */
export function parseTimestamp(value: string): Date {
  return new Date(/(?:Z|[+-]\d{2}:\d{2})$/i.test(value) ? value : `${value}Z`);
}
export function formatTimestamp(value: string): string {
  return parseTimestamp(value).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}
