import { Send } from "lucide-react";
import { FormEvent, KeyboardEvent, useState } from "react";

type BONInputProps = {
  disabled?: boolean;
  onSend: (message: string) => void;
};

function BONInput({ disabled = false, onSend }: BONInputProps) {
  const [message, setMessage] = useState("");

  function submitMessage() {
    const trimmedMessage = message.trim();

    if (!trimmedMessage || disabled) {
      return;
    }

    onSend(trimmedMessage);
    setMessage("");
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    submitMessage();
  }

  function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      submitMessage();
    }
  }

  return (
    <form className="bon-input" onSubmit={handleSubmit}>
      <textarea
        aria-label="Message BON"
        disabled={disabled}
        rows={1}
        placeholder="Ask BON about your vehicle..."
        value={message}
        onChange={(event) => setMessage(event.target.value)}
        onKeyDown={handleKeyDown}
      />
      <button
        aria-label="Send message"
        className="bon-input__send"
        disabled={disabled || !message.trim()}
        type="submit"
      >
        <Send size={18} />
      </button>
    </form>
  );
}

export default BONInput;
