import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/* =====================================
   NORMALIZE MODEL OUTPUT
===================================== */

function normalizeMarkdown(content) {

  if (typeof content !== "string") {

    return "";

  }

  return content

    // =================================
    // LINE BREAK
    // =================================

    .replace(
      /<br\s*\/?>/gi,
      "\n"
    )

    // =================================
    // UNORDERED LIST
    // =================================

    .replace(
      /<ul[^>]*>/gi,
      "\n"
    )

    .replace(
      /<\/ul>/gi,
      "\n"
    )

    .replace(
      /<li[^>]*>/gi,
      "\n- "
    )

    .replace(
      /<\/li>/gi,
      ""
    )

    // =================================
    // ORDERED LIST
    // =================================

    .replace(
      /<ol[^>]*>/gi,
      "\n"
    )

    .replace(
      /<\/ol>/gi,
      "\n"
    )

    // =================================
    // PARAGRAPH
    // =================================

    .replace(
      /<p[^>]*>/gi,
      "\n"
    )

    .replace(
      /<\/p>/gi,
      "\n"
    )

    // =================================
    // BOLD
    // =================================

    .replace(
      /<strong[^>]*>/gi,
      "**"
    )

    .replace(
      /<\/strong>/gi,
      "**"
    )

    .replace(
      /<b[^>]*>/gi,
      "**"
    )

    .replace(
      /<\/b>/gi,
      "**"
    )

    // =================================
    // ITALIC
    // =================================

    .replace(
      /<em[^>]*>/gi,
      "*"
    )

    .replace(
      /<\/em>/gi,
      "*"
    )

    .replace(
      /<i[^>]*>/gi,
      "*"
    )

    .replace(
      /<\/i>/gi,
      "*"
    )

    // =================================
    // REMOVE REMAINING HTML TAGS
    // =================================

    .replace(
      /<[^>]+>/g,
      ""
    )

    // =================================
    // CLEAN EXCESSIVE NEWLINES
    // =================================

    .replace(
      /\n{3,}/g,
      "\n\n"
    )

    .trim();

}


/* =====================================
   MARKDOWN MESSAGE
===================================== */

export default function MarkdownMessage({

  content = "",

}) {

  const normalizedContent =
    normalizeMarkdown(
      content
    );

  return (

    <ReactMarkdown

      remarkPlugins={[
        remarkGfm,
      ]}

      components={{

        // =============================
        // PARAGRAPH
        // =============================

        p({

          children,

        }) {

          return (

            <p>

              {children}

            </p>

          );

        },

        // =============================
        // TABLE WRAPPER
        // =============================

        table({

          children,

        }) {

          return (

            <div
              className=
                "markdown-table-wrapper"
            >

              <table>

                {children}

              </table>

            </div>

          );

        },

        // =============================
        // TABLE HEAD
        // =============================

        thead({

          children,

        }) {

          return (

            <thead>

              {children}

            </thead>

          );

        },

        // =============================
        // TABLE BODY
        // =============================

        tbody({

          children,

        }) {

          return (

            <tbody>

              {children}

            </tbody>

          );

        },

        // =============================
        // TABLE ROW
        // =============================

        tr({

          children,

        }) {

          return (

            <tr>

              {children}

            </tr>

          );

        },

        // =============================
        // TABLE HEADER
        // =============================

        th({

          children,

        }) {

          return (

            <th>

              {children}

            </th>

          );

        },

        // =============================
        // TABLE CELL
        // =============================

        td({

          children,

        }) {

          return (

            <td>

              {children}

            </td>

          );

        },

        // =============================
        // UNORDERED LIST
        // =============================

        ul({

          children,

        }) {

          return (

            <ul>

              {children}

            </ul>

          );

        },

        // =============================
        // ORDERED LIST
        // =============================

        ol({

          children,

        }) {

          return (

            <ol>

              {children}

            </ol>

          );

        },

        // =============================
        // LIST ITEM
        // =============================

        li({

          children,

        }) {

          return (

            <li>

              {children}

            </li>

          );

        },

        // =============================
        // CODE BLOCK
        // =============================

        code({

          className,

          children,

          ...props

        }) {

          const isBlock =
            Boolean(className);

          if (isBlock) {

            return (

              <pre>

                <code
                  className={
                    className
                  }
                  {...props}
                >

                  {children}

                </code>

              </pre>

            );

          }

          return (

            <code
              {...props}
            >

              {children}

            </code>

          );

        },

      }}

    >

      {normalizedContent}

    </ReactMarkdown>

  );

}