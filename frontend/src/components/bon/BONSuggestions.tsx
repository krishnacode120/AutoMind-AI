const SUGGESTIONS = [
  "How is my car?",
  "Any active alerts?",
  "Do I need maintenance?",
  "Show latest telemetry.",
  "What is my health score?",
];

type BONSuggestionsProps = {
  disabled?: boolean;
  onSelect: (question: string) => void;
};

function BONSuggestions({ disabled = false, onSelect }: BONSuggestionsProps) {
  return (
    <div className="bon-suggestions" aria-label="Suggested questions">
      {SUGGESTIONS.map((suggestion) => (
        <button
          className="bon-suggestion"
          disabled={disabled}
          key={suggestion}
          type="button"
          onClick={() => onSelect(suggestion)}
        >
          {suggestion}
        </button>
      ))}
    </div>
  );
}

export default BONSuggestions;
