import React from "react";

const MessageBubble = ({
  role,
  content,
  setActiveCitation
}) => {

  // =====================================
  // PARSE INLINE CITATIONS
  // =====================================

  const renderContent = (text) => {

    const parts = text.split(/(\[\d+\])/g);

    return parts.map((part, index) => {

      const match = part.match(/\[(\d+)\]/);

      // =================================
      // CITATION
      // =================================

      if (match) {

        const citationId = Number(match[1]);

        return (
          <span
            key={index}
            className="inline-citation"
            onClick={() =>
              setActiveCitation(citationId)
            }
          >
            {part}
          </span>
        );
      }

      // =================================
      // NORMAL TEXT
      // =================================

      return (
        <span key={index}>
          {part}
        </span>
      );
    });
  };

  return (
    <div className={`message ${role}`}>

      <div className="message-content">

        {renderContent(content)}

      </div>

    </div>
  );
};

export default MessageBubble;