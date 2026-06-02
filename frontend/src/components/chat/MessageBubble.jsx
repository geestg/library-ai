import React from "react";

import ReactMarkdown from "react-markdown";

import remarkGfm from "remark-gfm";

import {
  renderCitationText
} from "../../utils/citationParser.jsx";

export default function MessageBubble({
  role,
  content,
  citations,
  evidence,
  setActiveCitation
}) {
  return (
    <div
      className={`message ${role}`}
    >
      <div className="message-content">
        <ReactMarkdown
          remarkPlugins={[
            remarkGfm
          ]}
          components={{
            p({
              children
            }) {
              return (
                <p>
                  {React.Children.map(
                    children,
                    (child) => {
                      if (
                        typeof child ===
                        "string"
                      ) {
                        return renderCitationText(
                          child,
                          setActiveCitation
                        );
                      }

                      return child;
                    }
                  )}
                </p>
              );
            },

            li({
              children
            }) {
              return (
                <li>
                  {React.Children.map(
                    children,
                    (child) => {
                      if (
                        typeof child ===
                        "string"
                      ) {
                        return renderCitationText(
                          child,
                          setActiveCitation
                        );
                      }

                      return child;
                    }
                  )}
                </li>
              );
            }
          }}
        >
          {content}
        </ReactMarkdown>
      </div>
    </div>
  );
}