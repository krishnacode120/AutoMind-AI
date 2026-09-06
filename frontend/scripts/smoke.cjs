const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");

async function main() {
  const browser = await chromium.launch({
    headless: true,
    channel: process.env.PLAYWRIGHT_CHANNEL || undefined,
  });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
  });
  const page = await context.newPage();
  const frontend = process.env.FRONTEND_URL || "http://127.0.0.1:5173";
  const backend = process.env.API_URL || "http://127.0.0.1:8000/api/v1";
  const ids = [];
  const errors = [];
  const streams = [];
  const artifacts = path.resolve(__dirname, "../../.runtime");
  fs.mkdirSync(artifacts, { recursive: true });
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("websocket", (socket) =>
    socket.on("framereceived", (frame) => streams.push(String(frame.payload))),
  );
  const name = `Browser test ${Date.now()}`;
  async function navigate(label) {
    await page.getByRole("link", { name: label, exact: true }).click();
    await page
      .getByRole("heading", { level: 1, name: label, exact: true })
      .waitFor();
  }
  async function createVehicle(vehicleName) {
    await navigate("Vehicles");
    await page
      .getByRole("button", { name: "Add vehicle", exact: true })
      .click();
    await page.getByLabel("Vehicle name", { exact: true }).fill(vehicleName);
    await page.getByLabel("Manufacturer", { exact: true }).fill("Toyota");
    await page.getByLabel("Model", { exact: true }).fill("Corolla");
    const response = page.waitForResponse(
      (r) => r.url().endsWith("/vehicles") && r.request().method() === "POST",
    );
    await page.getByRole("button", { name: "Save vehicle" }).click();
    const saved = await response;
    assert.equal(saved.status(), 201);
    const id = (await saved.json()).data.id;
    ids.push(id);
    await page.locator("dialog").waitFor({ state: "hidden" });
    return id;
  }
  try {
    await page.goto(frontend);
    const first = await createVehicle(name);
    await page
      .getByRole("button", { name: `Edit ${name}`, exact: true })
      .click();
    await page
      .getByLabel("Vehicle name", { exact: true })
      .fill(name + " edited");
    await page.getByRole("button", { name: "Save vehicle" }).click();
    await page.locator("dialog").waitFor({ state: "hidden" });
    await navigate("Dashboard");
    await page.getByText("Connected", { exact: true }).waitFor();
    await page
      .getByRole("button", { name: "Simulate drive", exact: true })
      .click();
    await page
      .getByText("60 simulated readings recorded.", { exact: true })
      .waitFor();
    await page.locator(".recharts-line-curve").first().waitFor();
    assert.ok(
      streams.some((message) => message.includes("telemetry_update")),
      "No telemetry WebSocket event received",
    );
    await page.screenshot({
      path: path.join(artifacts, "dashboard-desktop.png"),
      fullPage: true,
    });
    await page.getByRole("button", { name: "Switch to dark theme" }).click();
    await page.reload();
    await page.getByRole("button", { name: "Switch to light theme" }).waitFor();
    assert.equal(await page.locator("html").getAttribute("data-theme"), "dark");
    await page.screenshot({
      path: path.join(artifacts, "dashboard-dark.png"),
      fullPage: true,
    });
    await page.getByRole("button", { name: "Switch to light theme" }).click();
    await navigate("Telemetry");
    await page.locator(".telemetry-table tbody tr").first().waitFor();
    assert.equal(await page.locator(".telemetry-table tbody tr").count(), 20);
    const downloadEvent = page.waitForEvent("download");
    await page.getByRole("button", { name: "Export page CSV" }).click();
    const download = await downloadEvent;
    const exported = path.join(artifacts, "telemetry-export.csv");
    await download.saveAs(exported);
    const csv = fs.readFileSync(exported, "utf8");
    assert.ok(csv.includes("battery_voltage"));
    assert.equal(csv.trim().split("\r\n").length, 21);
    await page.getByRole("button", { name: "Next readings page" }).click();
    await page
      .getByText("Page 2 · 20 readings per page", { exact: true })
      .waitFor();
    await navigate("Dashboard");
    await page.getByLabel("Simulation scenario").selectOption("overheating");
    await page
      .getByRole("button", { name: "Simulate drive", exact: true })
      .click();
    await page
      .getByText("60 simulated readings recorded.", { exact: true })
      .waitFor();
    await navigate("Alerts");
    await page
      .getByRole("heading", { name: "High engine temperature", exact: true })
      .waitFor();
    await page.getByRole("button", { name: "critical", exact: true }).click();
    assert.equal(await page.locator(".alert-detail").count(), 1);
    await navigate("Dashboard");
    for (const route of [
      "Telemetry",
      "Health",
      "Alerts",
      "Maintenance",
      "Predictions",
      "Settings",
    ]) {
      await page.getByRole("link", { name: route, exact: true }).click();
      await page
        .getByRole("heading", { level: 1, name: route, exact: true })
        .waitFor();
    }
    await navigate("BON");
    await page.getByLabel("Message BON").fill("How is my car?");
    await page.getByLabel("Message BON").press("Enter");
    await page.locator(".bon-message--assistant").first().waitFor();
    assert.match(
      await page.locator(".bon-message--assistant").innerText(),
      /health/i,
    );
    await page.reload();
    await page.locator(".bon-message--assistant").first().waitFor();
    await createVehicle(name + " second");
    await navigate("BON");
    assert.equal(
      await page.locator(".bon-message--assistant").count(),
      0,
      "Conversation leaked between vehicles",
    );
    await page.getByLabel("Selected vehicle").selectOption(String(first));
    await page.locator(".bon-message--assistant").first().waitFor();
    await page.getByRole("button", { name: "Clear conversation" }).click();
    await page.locator(".bon-message--assistant").waitFor({ state: "hidden" });
    await page.setViewportSize({ width: 390, height: 844 });
    for (const route of [
      "Vehicles",
      "Dashboard",
      "Telemetry",
      "Health",
      "Alerts",
      "Maintenance",
      "Predictions",
      "Settings",
      "BON",
    ]) {
      await page.getByRole("link", { name: route, exact: true }).click();
      await page
        .getByRole("heading", { level: 1, name: route, exact: true })
        .waitFor();
      assert.ok(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth + 1,
        ),
        `${route} overflows on mobile`,
      );
      await page.screenshot({
        path: path.join(artifacts, `${route.toLowerCase()}-mobile.png`),
        fullPage: true,
      });
    }
    await navigate("Vehicles");
    await page
      .getByRole("button", { name: `Delete ${name} edited`, exact: true })
      .click();
    await page
      .getByRole("button", { name: "Confirm delete", exact: true })
      .click();
    await page
      .getByRole("button", { name: `Delete ${name} edited`, exact: true })
      .waitFor({ state: "hidden" });
    assert.deepEqual(errors, []);
    console.log(
      "PASS: CRUD, scenarios, WebSocket, CSV, history, themes, all pages, BON persistence/clear/isolation, desktop and mobile.",
    );
  } catch (error) {
    await page
      .screenshot({
        path: path.join(artifacts, "browser-failure.png"),
        fullPage: true,
      })
      .catch(() => {});
    throw error;
  } finally {
    for (const id of ids)
      await context.request.delete(`${backend}/vehicles/${id}`).catch(() => {});
    await browser.close();
  }
}
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
