# Developer scripts

Run `python scripts/dev.py` from the repository root using the Python environment
where you installed `requirements-dev.txt`. Install frontend dependencies with
`npm ci` in `frontend/` first.

Optional flags: `--backend-port 8100 --frontend-port 5180`.

The launcher checks those ports, starts both services, configures the frontend
proxy, and stops its children on Ctrl+C or a child process failure. It does not
terminate pre-existing services.

The isolated browser launcher lives in `frontend/scripts/e2e.cjs` and runs
through `npm run test:e2e`.
