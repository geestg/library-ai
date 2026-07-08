import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function normalizeMarkdown(content) {
  if (typeof content !== "string") {
    return "";
  }

  return content
    .replace(/\r\n?/g, "\n")
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<ul[^>]*>/gi, "\n")
    .replace(/<\/ul>/gi, "\n")
    .replace(/<ol[^>]*>/gi, "\n")
    .replace(/<\/ol>/gi, "\n")
    .replace(/<li[^>]*>/gi, "\n- ")
    .replace(/<\/li>/gi, "")
    .replace(/<p[^>]*>/gi, "\n")
    .replace(/<\/p>/gi, "\n")
    .replace(/<strong[^>]*>/gi, "**")
    .replace(/<\/strong>/gi, "**")
    .replace(/<b[^>]*>/gi, "**")
    .replace(/<\/b>/gi, "**")
    .replace(/<em[^>]*>/gi, "*")
    .replace(/<\/em>/gi, "*")
    .replace(/<i[^>]*>/gi, "*")
    .replace(/<\/i>/gi, "*")
    .replace(/<[^>]+>/g, "")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function getCodeText(children) {
  return String(children ?? "").replace(/\n$/, "");
}

export default function MarkdownMessage({
  content = "",
  onCitationClick,
}) {
  const normalizedContent =
    normalizeMarkdown(content);

  return (
    <div className="markdown-message">
      <ReactMarkdown
        remarkPlugins={[
          remarkGfm,
        ]}
        components={{
          h1({ children }) {
            return (
              <h1 className="markdown-heading markdown-heading-1">
                {children}
              </h1>
            );
          },

          h2({ children }) {
            return (
              <h2 className="markdown-heading markdown-heading-2">
                {children}
              </h2>
            );
          },

          h3({ children }) {
            return (
              <h3 className="markdown-heading markdown-heading-3">
                {children}
              </h3>
            );
          },

          h4({ children }) {
            return (
              <h4 className="markdown-heading markdown-heading-4">
                {children}
              </h4>
            );
          },

          p({ children }) {
            return (
              <p className="markdown-paragraph">
                {children}
              </p>
            );
          },

          strong({ children }) {
            return (
              <strong className="markdown-strong">
                {children}
              </strong>
            );
          },

          em({ children }) {
            return (
              <em className="markdown-emphasis">
                {children}
              </em>
            );
          },

          a({
            href,
            children,
            ...props
          }) {
            return (
              <a
                className="markdown-link"
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                {...props}
              >
                {children}
              </a>
            );
          },

          blockquote({ children }) {
            return (
              <blockquote className="markdown-blockquote">
                {children}
              </blockquote>
            );
          },

          hr() {
            return (
              <hr className="markdown-divider" />
            );
          },

          ul({ children }) {
            return (
              <ul className="markdown-list markdown-list-unordered">
                {children}
              </ul>
            );
          },

          ol({ children }) {
            return (
              <ol className="markdown-list markdown-list-ordered">
                {children}
              </ol>
            );
          },

          li({ children }) {
            return (
              <li className="markdown-list-item">
                {children}
              </li>
            );
          },

          table({ children }) {
            return (
              <div
                className="markdown-table-wrapper"
                role="region"
                aria-label="Tabel hasil analisis"
                tabIndex={0}
              >
                <table className="markdown-table">
                  {children}
                </table>
              </div>
            );
          },

          thead({ children }) {
            return (
              <thead className="markdown-table-head">
                {children}
              </thead>
            );
          },

          tbody({ children }) {
            return (
              <tbody className="markdown-table-body">
                {children}
              </tbody>
            );
          },

          tr({ children }) {
            return (
              <tr className="markdown-table-row">
                {children}
              </tr>
            );
          },

          th({ children }) {
            return (
              <th
                className="markdown-table-header"
                scope="col"
              >
                {children}
              </th>
            );
          },

          td({ children }) {
            return (
              <td className="markdown-table-cell">
                {children}
              </td>
            );
          },

          code({
            inline,
            className,
            children,
            ...props
          }) {
            const codeText =
              getCodeText(children);

            if (!inline) {
              return (
                <code
                  className={[
                    "markdown-code-block",
                    className,
                  ]
                    .filter(Boolean)
                    .join(" ")}
                  {...props}
                >
                  {codeText}
                </code>
              );
            }

            return (
              <code
                className="markdown-inline-code"
                {...props}
              >
                {children}
              </code>
            );
          },

          pre({ children }) {
            return (
              <pre className="markdown-pre">
                {children}
              </pre>
            );
          },

          img({
            src,
            alt = "",
            ...props
          }) {
            return (
              <img
                className="markdown-image"
                src={src}
                alt={alt}
                loading="lazy"
                {...props}
              />
            );
          },
        }}
      >
        {normalizedContent}
      </ReactMarkdown>
    </div>
  );
}