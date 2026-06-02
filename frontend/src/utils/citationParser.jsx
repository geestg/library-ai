import React from "react";

export function renderCitationText(
  text,
  setActiveCitation
) {
  if (!text) return text;

  const regex = /\[(\d+)\]/g;

  const parts = [];

  let lastIndex = 0;

  let match;

  while (
    (match = regex.exec(text)) !== null
  ) {
    const citationId = Number(
      match[1]
    );

    if (match.index > lastIndex) {
      parts.push(
        text.slice(
          lastIndex,
          match.index
        )
      );
    }

    parts.push(
      <button
        key={`citation-${citationId}-${match.index}`}
        className="inline-citation"
        onClick={() =>
          setActiveCitation?.(
            citationId
          )
        }
      >
        [{citationId}]
      </button>
    );

    lastIndex = regex.lastIndex;
  }

  if (lastIndex < text.length) {
    parts.push(
      text.slice(lastIndex)
    );
  }

  return parts;
}