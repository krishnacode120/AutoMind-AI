import { Component, type ReactNode, type ErrorInfo } from "react";
export default class ErrorBoundary extends Component<
  { children: ReactNode },
  { failed: boolean }
> {
  state = { failed: false };
  static getDerivedStateFromError() {
    return { failed: true };
  }
  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("AutoMind render failed", error, info);
  }
  render() {
    return this.state.failed ? (
      <main className="error-boundary">
        <h1>Something interrupted your workspace.</h1>
        <p>Reload the page to reconnect to your vehicle data.</p>
        <button
          className="action-button primary"
          onClick={() => window.location.reload()}
        >
          Reload workspace
        </button>
      </main>
    ) : (
      this.props.children
    );
  }
}
