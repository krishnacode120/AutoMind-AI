# AutoMind frontend

React, TypeScript, Vite, TanStack Query, Recharts, Lucide, and React Hook Form.

```sh
npm ci
npm run dev
npm run build
```

Node.js 22.12+ is required. The default API base is `/api/v1`; Vite proxies
`/api` (including WebSockets) to `http://127.0.0.1:8000`. Set the process
variable `VITE_PROXY_TARGET` for a different backend. Docker uses nginx with
equivalent routing.

`npm run test:e2e` starts isolated services and runs Playwright. Install Chromium
with `npx playwright install chromium`, or set `PLAYWRIGHT_CHANNEL=msedge`
on Windows. Use `npm run test:e2e:running` to verify existing services.

See the [root README](../README.md) for complete setup and behavior.
