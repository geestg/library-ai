import React from "react";

import ReactMarkdown from "react-markdown";

import remarkGfm from "remark-gfm";

import {
  FileText
} from "lucide-react";

import {
  renderCitationText
} from "../../utils/citationParser.jsx";

export default function MessageBubble({

  role,

  content,

  citations,

  evidence,

  attachedDocuments = [],

  setActiveCitation

}) {

  return (

    <div
      className={`message ${role}`}
    >

      <div className="message-content">

        {

          role === "user"

          &&

          attachedDocuments.length > 0

          && (

            <div
              className="
              message-document-list
              "
            >

              {

                attachedDocuments.map(

                  (doc) => (

                    <div

                      key={
                        doc.document_id
                          ||
                        doc.filename
                      }

                      className="
                      message-document-pill
                      "

                    >

                      <FileText
                        size={14}
                      />

                      <span>

                        {
                          doc.filename
                        }

                      </span>

                    </div>

                  )

                )

              }

            </div>

          )

        }

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

                  {

                    React.Children.map(

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

                    )

                  }

                </p>

              );

            },

            li({
              children
            }) {

              return (

                <li>

                  {

                    React.Children.map(

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

                    )

                  }

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