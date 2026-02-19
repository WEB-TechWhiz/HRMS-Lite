export default function ErrorState({ message, onRetry }) {
  return (
    <div>
      <p>{message}</p>
      <button type="button" onClick={onRetry}>Retry</button>
    </div>
  );
}
