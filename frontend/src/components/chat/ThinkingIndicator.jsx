export default function ThinkingIndicator() {

  return (

    <div

      className="modern-thinking"

      role="status"

      aria-live="polite"

      aria-label="Sedang menganalisis"

    >

      <div

        className="thinking-loader"

        aria-hidden="true"

      >

        <span className="thinking-dot" />

        <span className="thinking-dot" />

        <span className="thinking-dot" />

      </div>

      <span className="thinking-label">

        Menganalisis konteks penelitian

      </span>

    </div>

  );

}