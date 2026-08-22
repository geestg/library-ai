import React from "react";

import ReactMarkdown from "react-markdown";

import remarkGfm from "remark-gfm";

import {
  parseCitations
} from "../../utils/citationParser.jsx";

function CitationText({

  children,

  onCitationClick

}) {

  return (

    <>

      {

        React.Children.map(

          children,

          (child) => {

            if (

              typeof child ===
              "string"

            ) {

              return parseCitations(

                child,

                onCitationClick

              );

            }

            return child;

          }

        )

      }

    </>

  );

}

export default function MarkdownMessage({

  content,

  onCitationClick

}) {

  return (
    <div className="message-content">
      <ReactMarkdown
        remarkPlugins={[
          remarkGfm
        ]}
        components={{

          p(props) {

            return (

              <p>

                <CitationText

                  onCitationClick={
                    onCitationClick
                  }

                >

                  {
                    props.children
                  }

                </CitationText>

              </p>

            );

          },

          li(props) {

            return (

              <li>

                <CitationText

                  onCitationClick={
                    onCitationClick
                  }

                >

                  {
                    props.children
                  }

                </CitationText>

              </li>

            );

          },

          td(props) {

            return (

              <td>

                <CitationText

                  onCitationClick={
                    onCitationClick
                  }

                >

                  {
                    props.children
                  }

                </CitationText>

              </td>

            );

          },

          th(props) {

            return (

              <th>

                <CitationText

                  onCitationClick={
                    onCitationClick
                  }

                >

                  {
                    props.children
                  }

                </CitationText>

              </th>

            );

          },

          strong(props) {

            return (

              <strong>

                <CitationText

                  onCitationClick={
                    onCitationClick
                  }

                >

                  {
                    props.children
                  }

                </CitationText>

              </strong>

            );

          }

        }}

      >

        {content}

      </ReactMarkdown>
    </div>
  );
}