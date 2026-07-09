export default function ThinkingIndicator({

  progress = null,

}) {

  // =====================================
  // RESOLVE LABEL
  // =====================================

  const label =

    progress?.label ||

    "Menganalisis konteks penelitian";

  // =====================================
  // RESOLVE PHASE
  // =====================================

  const phase =

    progress?.phase ||

    "thinking";

  // =====================================
  // UI
  // =====================================

  return (

    <div

      className="modern-thinking"

      role="status"

      aria-live="polite"

      aria-label={label}

      data-phase={phase}

    >

      <div

        className="thinking-loader"

        aria-hidden="true"

      >

        <span className="thinking-dot" />

        <span className="thinking-dot" />

        <span className="thinking-dot" />

      </div>

      <span

        className="thinking-label"

      >

        {label}

      </span>

    </div>

  );

}