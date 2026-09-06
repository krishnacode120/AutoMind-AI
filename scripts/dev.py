"""Run the API and Vite together: python scripts/dev.py."""

import argparse
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def ensure_free(port: int) -> None:
    with socket.socket() as probe:
        try:
            probe.bind(("127.0.0.1", port))
        except OSError:
            raise SystemExit(
                f"Port {port} is already in use. Choose another port."
            ) from None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend-port", type=int, default=8000)
    parser.add_argument("--frontend-port", type=int, default=5173)
    args = parser.parse_args()
    if args.backend_port == args.frontend_port:
        parser.error("Backend and frontend ports must differ.")
    for port in (args.backend_port, args.frontend_port):
        if not 1 <= port <= 65535:
            parser.error("Ports must be between 1 and 65535.")
        ensure_free(port)
    node = shutil.which("node")
    vite = ROOT / "frontend/node_modules/vite/bin/vite.js"
    if not node or not vite.exists():
        raise SystemExit("Install Node.js 22.12+ and run npm ci in frontend first.")
    env = {
        **os.environ,
        "VITE_API_BASE_URL": "/api/v1",
        "VITE_WS_BASE_URL": "",
        "VITE_PROXY_TARGET": f"http://127.0.0.1:{args.backend_port}",
    }
    flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    children: list[subprocess.Popen] = []
    try:
        children.append(
            subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "uvicorn",
                    "app.main:app",
                    "--host",
                    "127.0.0.1",
                    "--port",
                    str(args.backend_port),
                ],
                cwd=ROOT / "backend",
                env=env,
                creationflags=flags,
            )
        )
        children.append(
            subprocess.Popen(
                [node, str(vite), "--port", str(args.frontend_port)],
                cwd=ROOT / "frontend",
                env=env,
                creationflags=flags,
            )
        )
        print(f"Workspace: http://127.0.0.1:{args.frontend_port}", flush=True)
        print(f"API docs: http://127.0.0.1:{args.backend_port}/docs", flush=True)
        print("Press Ctrl+C to stop both services.", flush=True)
        while all(child.poll() is None for child in children):
            time.sleep(0.5)
        return next(
            (child.returncode or 1 for child in children if child.poll() is not None), 1
        )
    except KeyboardInterrupt:
        return 0
    finally:
        for child in children:
            if child.poll() is None:
                child.terminate()
        for child in children:
            try:
                child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait()


if __name__ == "__main__":
    raise SystemExit(main())
