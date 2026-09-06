/** Quote CSV values and neutralize spreadsheet formulas in text cells. */
export function csvCell(value: unknown): string {
  const text = String(value ?? "");
  const safe =
    typeof value === "string" && /^[=+\-@\t\r]/.test(text) ? "'" + text : text;
  return '"' + safe.replaceAll('"', '""') + '"';
}
export function downloadCSV(
  name: string,
  rows: Record<string, unknown>[],
): void {
  if (!rows.length) return;
  const fields = Object.keys(rows[0]);
  const csv = [
    fields.map(csvCell).join(","),
    ...rows.map((row) => fields.map((key) => csvCell(row[key])).join(",")),
  ].join("\r\n");
  const url = URL.createObjectURL(
    new Blob(["\uFEFF" + csv], { type: "text/csv;charset=utf-8;" }),
  );
  const link = document.createElement("a");
  link.href = url;
  link.download = name;
  document.body.append(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
