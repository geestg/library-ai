import React from "react";

import ReactMarkdown from "react-markdown";

import remarkGfm from "remark-gfm";

export default function MessageBubble({

  role,

  content

}) {

  return (

    <div className={`message ${role}`}>

      <div className="message-content">

        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
        >

          {content || ""}

        </ReactMarkdown>

      </div>

    </div>
  );
}