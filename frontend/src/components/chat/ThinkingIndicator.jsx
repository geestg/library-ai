export default function ThinkingIndicator({

  progress = null,

}) {

  // =====================================
  // PROGRESS DATA
  // =====================================

  const phase =

    progress?.phase ??

    null;

  const stage =

    progress?.stage ??

    null;

  const label =

    progress?.label ??

    "Menganalisis konteks penelitian";

  // =====================================
  // ACCESSIBILITY LABEL
  // =====================================

  const accessibilityLabel =

    label ||

    "Sedang menganalisis";

  // =====================================
  // UI
  // =====================================

  return (

    <div

      className="modern-thinking"

      role="status"

      aria-live="polite"

      aria-label={
        accessibilityLabel
      }

      data-phase={
        phase ?? undefined
      }

      data-stage={
        stage ?? undefined
      }

    >

      {/* ================================= */}
      {/* LOADER */}
      {/* ================================= */}

      <div

        className="thinking-loader"

        aria-hidden="true"

      >

        <span className="thinking-dot" />

        <span className="thinking-dot" />

        <span className="thinking-dot" />

      </div>

      {/* ================================= */}
      {/* PROGRESS LABEL */}
      {/* ================================= */}

      <span className="thinking-label">

        {label}

      </span>

    </div>

  );

}