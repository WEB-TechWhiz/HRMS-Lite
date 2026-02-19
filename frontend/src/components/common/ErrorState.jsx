export default function ErrorState({ message, onRetry }) {
  return (
    <div className="state error" role="alert">
      <p>{message}</p>
      <div className="state-actions">
        <button className="btn btn-soft" type="button" onClick={onRetry}>Retry</button>
      </div>
    </div>
  );
}