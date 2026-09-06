// Starts isolated services and invokes the browser smoke suite. No developer DB access.
const { spawn } = require("node:child_process");
const { once } = require("node:events");
const fs = require("node:fs");
const net = require("node:net");
const path = require("node:path");

const root = path.resolve(__dirname, "../..");
const children = [];
const logs = [];
async function port() {
  const server = net.createServer();
  server.listen(0, "127.0.0.1");
  await once(server, "listening");
  const value = server.address().port;
  await new Promise((resolve) => server.close(resolve));
  return value;
}
function start(command, args, options) {
  const child = spawn(command, args, {
    windowsHide: true,
    stdio: ["ignore", "pipe", "pipe"],
    ...options,
  });
  child.on("error", (error) => logs.push(error.message));
  child.stdout.on("data", (data) => logs.push(String(data)));
  child.stderr.on("data", (data) => logs.push(String(data)));
  children.push(child);
  return child;
}
async function ready(url) {
  for (let attempt = 0; attempt < 100; attempt++) {
    if (children.some((child) => child.exitCode !== null))
      throw new Error("A test service exited before startup.");
    try {
      if ((await fetch(url, { signal: AbortSignal.timeout(1000) })).ok) return;
    } catch {}
    await new Promise((resolve) => setTimeout(resolve, 200));
  }
  throw new Error("Test service did not become ready: " + url);
}
async function main() {
  const runtime = path.join(root, ".runtime");
  fs.mkdirSync(runtime, { recursive: true });
  const directory = fs.mkdtempSync(path.join(runtime, "e2e-"));
  const backendPort = await port();
  let frontendPort = await port();
  while (frontendPort === backendPort) frontendPort = await port();
  const backend = "http://127.0.0.1:" + backendPort;
  const frontend = "http://127.0.0.1:" + frontendPort;
  const localPython = path.join(
    root,
    process.platform === "win32"
      ? ".venv/Scripts/python.exe"
      : ".venv/bin/python",
  );
  const python =
    process.env.PYTHON || (fs.existsSync(localPython) ? localPython : "python");
  const env = {
    ...process.env,
    DATABASE_URL:
      "sqlite:///" + path.join(directory, "test.db").replaceAll("\\", "/"),
    VITE_API_BASE_URL: "/api/v1",
    VITE_WS_BASE_URL: "",
    VITE_PROXY_TARGET: backend,
    FRONTEND_URL: frontend,
    API_URL: backend + "/api/v1",
    DEBUG: "False",
    TRUSTED_HOSTS: '["127.0.0.1","localhost","testserver"]',
  };
  try {
    start(
      python,
      [
        "-m",
        "uvicorn",
        "app.main:app",
        "--host",
        "127.0.0.1",
        "--port",
        String(backendPort),
      ],
      { cwd: path.join(root, "backend"), env },
    );
    start(
      process.execPath,
      [
        path.join(root, "frontend/node_modules/vite/bin/vite.js"),
        "--port",
        String(frontendPort),
      ],
      { cwd: path.join(root, "frontend"), env },
    );
    await Promise.all([ready(backend + "/api/v1/health"), ready(frontend)]);
    const test = spawn(process.execPath, [path.join(__dirname, "smoke.cjs")], {
      cwd: root,
      env,
      windowsHide: true,
      stdio: "inherit",
    });
    children.push(test);
    const [code] = await once(test, "exit");
    if (code !== 0) throw new Error("Browser verification failed.");
  } finally {
    for (const child of children) if (child.exitCode === null) child.kill();
    await Promise.all(
      children.map((child) =>
        child.exitCode !== null
          ? Promise.resolve()
          : Promise.race([
              once(child, "exit"),
              new Promise((resolve) => setTimeout(resolve, 3000)),
            ]),
      ),
    );
    fs.writeFileSync(path.join(directory, "services.log"), logs.join(""));
  }
}
main().catch((error) => {
  console.error(error.message);
  console.error(logs.slice(-15).join(""));
  process.exitCode = 1;
});
