import React from "react";

import ReactMarkdown from "react-markdown";

import remarkGfm from "remark-gfm";

import {
  FileText
} from "lucide-react";

import MarkdownMessage from "./MarkdownMessage";

import NoveltyCard from "./NoveltyCard";

export default function MessageBubble({

  role,

  content,

  citations,

  evidence,

  noveltyAnalysis,

  attachedDocuments = [],

  setActiveCitation,

  setSelectedThesis,

  sources = []

}) {

  const handleCitationClick = (
    citationId
  ) => {

    setActiveCitation?.(
      citationId
    );

    const source = sources.find(

      (item) =>

        item.source_id ===
        citationId

    );

    if (source) {

      setSelectedThesis?.(
        source
      );

    }

  };

  return (

    <div
      className={`message ${role}`}
    >

      <div
        className="
        message-content
        markdown-body
        "
      >

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

        {

          role === "assistant"

          ? (

            <>

              <MarkdownMessage

                content={content}

                onCitationClick={
                  handleCitationClick
                }

              />

              <NoveltyCard

                noveltyAnalysis={
                  noveltyAnalysis
                }

              />

            </>

          )

          : (

            <ReactMarkdown

              remarkPlugins={[
                remarkGfm
              ]}

            >

              {content}

            </ReactMarkdown>

          )

        }

      </div>

    </div>

  );

}