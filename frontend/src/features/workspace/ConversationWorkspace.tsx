import {
    Fragment,
    useEffect,
    useMemo,
    useRef,
    useState,
} from "react";
import type {
    ReactNode,
} from "react";
import {
    Bot,
    ExternalLink,
    UserRound,
} from "lucide-react";

import {
    researchAnswer,
} from "../../api/research";
import ResearchInputDock from "./ResearchInputDock";
import {
    THREAD_SELECTED_EVENT,
    conversationTitle,
    ensureActiveThread,
    loadConversationThreads,
    saveConversationThread,
} from "./conversationHistory";
import type {
    CitationRecord,
    ConversationMessage,
    ConversationThread,
} from "./conversationHistory";

import "./ConversationWorkspace.css";

function messageId(prefix: string): string {
    if (
        typeof crypto !== "undefined" &&
        typeof crypto.randomUUID === "function"
    ) {
        return `${prefix}-${crypto.randomUUID()}`;
    }

    return (
        `${prefix}-${Date.now()}-` +
        Math.random().toString(36).slice(2)
    );
}

function inlineContent(
    value: string,
): ReactNode[] {
    const parts = value.split(
        /(\*\*[^*]+\*\*|`[^`]+`)/g,
    );

    return parts
        .filter(Boolean)
        .map((part, index) => {
            if (
                part.startsWith("**") &&
                part.endsWith("**")
            ) {
                return (
                    <strong key={index}>
                        {part.slice(2, -2)}
                    </strong>
                );
            }

            if (
                part.startsWith("`") &&
                part.endsWith("`")
            ) {
                return (
                    <code key={index}>
                        {part.slice(1, -1)}
                    </code>
                );
            }

            return (
                <Fragment key={index}>
                    {part}
                </Fragment>
            );
        });
}

function RichText({
    content,
}: {
    content: string;
}) {
    const blocks = useMemo(
        () =>
            content
                .replace(/\r\n/g, "\n")
                .split("\n"),
        [content],
    );

    return (
        <div className="delbot-rich-text">
            {blocks.map((line, index) => {
                const trimmed = line.trim();

                if (!trimmed) {
                    return (
                        <div
                            key={index}
                            className="delbot-text-space"
                        />
                    );
                }

                if (/^[-*_]{3,}$/.test(trimmed)) {
                    return <hr key={index} />;
                }

                const heading =
                    trimmed.match(
                        /^(#{1,3})\s+(.+)$/,
                    );

                if (heading) {
                    return (
                        <div
                            key={index}
                            className="delbot-text-heading"
                        >
                            {inlineContent(
                                heading[2],
                            )}
                        </div>
                    );
                }

                const bullet =
                    trimmed.match(
                        /^[-•◆▪]\s+(.+)$/,
                    );

                if (bullet) {
                    return (
                        <div
                            key={index}
                            className="delbot-text-list-row"
                        >
                            <span
                                className="delbot-text-bullet"
                                aria-hidden="true"
                            >
                                •
                            </span>
                            <span>
                                {inlineContent(
                                    bullet[1],
                                )}
                            </span>
                        </div>
                    );
                }

                const numbered =
                    trimmed.match(
                        /^(\d+)[.)]\s+(.+)$/,
                    );

                if (numbered) {
                    return (
                        <div
                            key={index}
                            className="delbot-text-list-row"
                        >
                            <span className="delbot-text-number">
                                {numbered[1]}.
                            </span>
                            <span>
                                {inlineContent(
                                    numbered[2],
                                )}
                            </span>
                        </div>
                    );
                }

                return (
                    <p key={index}>
                        {inlineContent(trimmed)}
                    </p>
                );
            })}
        </div>
    );
}

function citationTitle(
    citation: CitationRecord,
): string {
    return (
        citation.document?.title ||
        citation.document_title ||
        citation.document?.document_id ||
        citation.document_id ||
        "Sumber repository"
    );
}

function CitationList({
    citations,
}: {
    citations: CitationRecord[];
}) {
    if (citations.length === 0) {
        return null;
    }

    return (
        <details className="delbot-citations">
            <summary>
                {citations.length} sumber
                {citations.length === 1
                    ? " repository"
                    : " repository"}
            </summary>

            <div className="delbot-citation-list">
                {citations.map(
                    (citation, index) => (
                        <div
                            key={
                                `${citationTitle(
                                    citation,
                                )}-${index}`
                            }
                            className="delbot-citation-card"
                        >
                            <div className="delbot-citation-index">
                                {index + 1}
                            </div>

                            <div className="delbot-citation-copy">
                                <strong>
                                    {citationTitle(
                                        citation,
                                    )}
                                </strong>

                                <span>
                                    {citation.page
                                        ? `Page ${citation.page}`
                                        : "Repository evidence"}
                                </span>

                                {citation.text ? (
                                    <p>
                                        {citation.text
                                            .replace(
                                                /\s+/g,
                                                " ",
                                            )
                                            .trim()
                                            .slice(
                                                0,
                                                220,
                                            )}
                                        {citation.text.length >
                                        220
                                            ? "…"
                                            : ""}
                                    </p>
                                ) : null}
                            </div>

                            {citation.document
                                ?.file_path ? (
                                <ExternalLink
                                    size={14}
                                    aria-hidden="true"
                                />
                            ) : null}
                        </div>
                    ),
                )}
            </div>
        </details>
    );
}


function delbotIsGuidanceAnswer(
  value: unknown,
): boolean {
  const answer =
    typeof value === "string"
      ? value
      : String(value ?? "");

  return (
    /##\s+Panduan Memulai Skripsi/i.test(answer)
    || /###\s+Langkah pertama sekarang/i.test(answer)
  );
}

function Bubble({
    message,
}: {
    message: ConversationMessage;
}) {
    const isUser =
        message.role === "user";

    return (
        <article
            className={[
                "delbot-message",
                isUser
                    ? "delbot-message-user"
                    : "delbot-message-assistant",
            ].join(" ")}
        >
            <div
                className={[
                    "delbot-message-avatar",
                    isUser
                        ? "delbot-avatar-user"
                        : "delbot-avatar-assistant",
                ].join(" ")}
                aria-hidden="true"
            >
                {isUser ? (
                    <UserRound size={15} />
                ) : (
                    <Bot size={15} />
                )}
            </div>

            <div className="delbot-message-column">
                <div className="delbot-message-author">
                    {isUser ? "You" : "DELBot"}
                </div>

                <div className="delbot-message-bubble">
                    {!isUser
                    && delbotIsGuidanceAnswer(
                        message.content,
                    ) ? (
                    <div className="delbot-guidance-answer">
                        <DelbotInsightAnswerView
                            answer={sanitizeAssistantPresentation(
                                message.content,
                                Boolean(
                                    message.citations?.length,
                                ),
                            )}
                        />
                    </div>
                ) : (
                    <RichText
                        content={sanitizeAssistantPresentation(
                            message.content,
                            Boolean(
                                message.citations?.length,
                            ),
                        )}
                    />
                )}
                </div>

                {!isUser ? (
                    <CitationList
                        citations={
                            message.citations ?? []
                        }
                    />
                ) : null}
            </div>
        </article>
    );
}

// DELBOT MVP assistant presentation sanitizer
const sanitizeAssistantPresentation = (
  value: unknown,
  hasStructuredCitations: boolean,
): string => {
  const text = typeof value === "string"
    ? value
    : String(value ?? "");

  const cleaned = text
    .split(/\r?\n/)
    .filter((line) => !/^\s*svg\s*$/i.test(line))
    .filter((line) =>
      !hasStructuredCitations
      || !/^\s*(?:[-*]\s*)?(?:\*{0,2})?sumber(?:\s+pendukung)?(?:\*{0,2})?\s*:/i.test(line),
    )
    .join("\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();

  return cleaned;
};


// DELBOT MVP research insight workspace modal
type DelbotInsightEvidence = {
  key: string;
  title: string;
  documentId: string;
  evidenceType: string;
  section: string;
  page: string;
  excerpt: string;
  author: string;
  year: string;
  prodi: string;
  url: string;
  isFulltext: boolean;
};

function delbotInsightRecord(
  value: unknown,
): Record<string, unknown> | null {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    return null;
  }

  return value as Record<string, unknown>;
}

function delbotInsightDeepString(
  value: unknown,
  keys: string[],
  depth = 0,
): string {
  if (depth > 4) {
    return "";
  }

  const record = delbotInsightRecord(value);

  if (!record) {
    return "";
  }

  for (const key of keys) {
    const candidate = record[key];

    if (typeof candidate === "string" && candidate.trim()) {
      return candidate.trim();
    }

    if (
      typeof candidate === "number"
      && Number.isFinite(candidate)
    ) {
      return String(candidate);
    }
  }

  for (const candidate of Object.values(record)) {
    if (candidate && typeof candidate === "object") {
      const nested = delbotInsightDeepString(
        candidate,
        keys,
        depth + 1,
      );

      if (nested) {
        return nested;
      }
    }
  }

  return "";
}

function delbotInsightAnswer(message: unknown): string {
  const record = delbotInsightRecord(message);

  if (!record) {
    return "";
  }

  for (const key of ["answer", "content", "text", "message"]) {
    const candidate = record[key];

    if (typeof candidate === "string" && candidate.trim()) {
      return candidate
        .replace(/^\s*svg\s*$/gim, "")
        .trim();
    }

    if (Array.isArray(candidate)) {
      const combined = candidate
        .map((item) => {
          if (typeof item === "string") {
            return item;
          }

          const itemRecord = delbotInsightRecord(item);
          const itemText = itemRecord?.text ?? itemRecord?.content;

          return typeof itemText === "string" ? itemText : "";
        })
        .filter(Boolean)
        .join("\n");

      if (combined.trim()) {
        return combined
          .replace(/^\s*svg\s*$/gim, "")
          .trim();
      }
    }
  }

  return "";
}

function delbotInsightRole(message: unknown): string {
  const record = delbotInsightRecord(message);
  const role = record?.role ?? record?.sender ?? record?.author;

  return typeof role === "string" ? role.toLowerCase() : "";
}

function delbotInsightEvidence(
  message: unknown,
): DelbotInsightEvidence[] {
  const arrays: unknown[][] = [];
  const visited = new Set<unknown>();

  const visit = (value: unknown, depth: number) => {
    if (
      depth > 5
      || !value
      || typeof value !== "object"
      || visited.has(value)
    ) {
      return;
    }

    visited.add(value);

    if (Array.isArray(value)) {
      value.forEach((item) => visit(item, depth + 1));
      return;
    }

    const record = value as Record<string, unknown>;

    Object.entries(record).forEach(([key, candidate]) => {
      const normalized = key
        .toLowerCase()
        .replace(/[^a-z]/g, "");

      if (
        Array.isArray(candidate)
        && [
          "citations",
          "citation",
          "sources",
          "references",
          "evidence",
          "documents",
        ].includes(normalized)
      ) {
        arrays.push(candidate);
      }

      if (candidate && typeof candidate === "object") {
        visit(candidate, depth + 1);
      }
    });
  };

  visit(message, 0);

  const result: DelbotInsightEvidence[] = [];
  const seen = new Set<string>();

  arrays.flat().forEach((candidate, index) => {
    const record = delbotInsightRecord(candidate);

    if (!record) {
      return;
    }

    const title = delbotInsightDeepString(record, [
      "title",
      "document_title",
      "source_title",
      "filename",
      "file_name",
      "name",
    ]);

    const documentId = delbotInsightDeepString(record, [
      "document_id",
      "documentId",
      "doc_id",
      "source_id",
      "handle",
      "id",
    ]);

    const evidenceType = delbotInsightDeepString(record, [
      "evidence_type",
      "source_type",
      "content_type",
      "type",
    ]);

    const section = delbotInsightDeepString(record, [
      "section_title",
      "section",
      "heading",
      "chapter",
      "bab",
    ]);

    const page = delbotInsightDeepString(record, [
      "page_range",
      "page_number",
      "page",
      "pages",
      "page_start",
    ]);

    const excerpt = delbotInsightDeepString(record, [
      "excerpt",
      "snippet",
      "chunk_text",
      "content_text",
      "abstract",
      "summary",
      "text",
      "content",
    ]);

    // DELBOT MVP source explorer v2 helpers
    const author = delbotInsightDeepString(record, [
      "author",
      "authors",
      "creator",
      "penulis",
    ]);

    const year = delbotInsightDeepString(record, [
      "year",
      "publication_year",
      "issued",
      "tahun",
    ]);

    const prodi = delbotInsightDeepString(record, [
      "prodi",
      "study_program",
      "program_studi",
      "department",
    ]);

    const url = delbotInsightDeepString(record, [
      "url",
      "repository_url",
      "source_url",
      "handle_url",
      "uri",
    ]);

    const friendlyEvidenceType = delbotFriendlyEvidenceType(
      evidenceType || "Repository evidence",
    );

    const isFulltext = friendlyEvidenceType === "Isi PDF";

    if (!title && !documentId && !excerpt) {
      return;
    }

    const identity = [
      documentId,
      title,
      section,
      page,
      excerpt.slice(0, 100),
    ].join("|");

    if (seen.has(identity)) {
      return;
    }

    seen.add(identity);

    result.push({
      key: identity || `source-${index}`,
      title: title || `Dokumen ${index + 1}`,
      documentId: documentId || "Tidak tersedia",
      evidenceType: friendlyEvidenceType,
      section: section || "Tidak dicantumkan",
      page: page || "Tidak dicantumkan",
      excerpt: excerpt || "Cuplikan evidence tidak tersedia.",
      author: author || "",
      year: year || "",
      prodi: prodi || "",
      url,
      isFulltext,
    });
  });

  return result;
}

function delbotIsResearchResult(message: unknown): boolean {
  const role = delbotInsightRole(message);
  const answer = delbotInsightAnswer(message);
  const evidence = delbotInsightEvidence(message);

  if (delbotIsGuidanceAnswer(answer)) {
    return false;
  }

  if (
    role
    && !["assistant", "delbot", "bot", "ai"].includes(role)
  ) {
    return false;
  }

  if (answer.length < 250) {
    return false;
  }

  const researchTerms =
    /\b(literatur|studi|research gap|tesis|skripsi|tugas akhir|evidence|repository|dataset|metode|temuan|referensi|sumber pendukung|ide penelitian|ide ta)\b/i;

  const repositoryOverview =
    /(?:statistik|isi)\s+repository\s+delbot|menampilkan\s+dokumen\s+\*\*?\d+/i.test(
      answer,
    );

  if (evidence.length === 0 || repositoryOverview) {
    return false;
  }

  // DELBOT UI V3: only sourced research becomes an insight card.
  return researchTerms.test(answer);
}

function delbotInsightInline(text: string) {
  return text
    .split(/(\*\*[^*]+\*\*|\[[^\]]+\])/g)
    .filter(Boolean)
    .map((part, index) => {
      if (part.startsWith("**") && part.endsWith("**")) {
        return (
          <strong key={`${index}-${part}`}>
            {part.slice(2, -2)}
          </strong>
        );
      }

      if (part.startsWith("[") && part.endsWith("]")) {
        return (
          <span
            className="delbot-insight-reference"
            key={`${index}-${part}`}
          >
            {part}
          </span>
        );
      }

      return <span key={`${index}-${part}`}>{part}</span>;
    });
}


// DELBOT structured research reader 767919
function DelbotStructuredAnswerView({
  answer,
}: {
  answer: string;
}) {
  const lines = answer
    .replace(/^\s*svg\s*$/gim, "")
    .split(/\r?\n/);
  const blocks = [];
  let index = 0;

  const isTableRow = (value: string) =>
    /^\s*\|.*\|\s*$/.test(value);
  const isTableSeparator = (value: string) =>
    /^\s*\|(?:\s*:?-{3,}:?\s*\|)+\s*$/.test(value);
  const cells = (value: string) =>
    value
      .trim()
      .replace(/^\||\|$/g, "")
      .split("|")
      .map((cell) => cell.trim());

  while (index < lines.length) {
    const raw = lines[index];
    const line = raw.trim();

    if (!line) {
      index += 1;
      continue;
    }

    if (
      isTableRow(line)
      && index + 1 < lines.length
      && isTableSeparator(lines[index + 1])
    ) {
      const header = cells(line);
      const rows = [];
      index += 2;
      while (index < lines.length && isTableRow(lines[index])) {
        rows.push(cells(lines[index]));
        index += 1;
      }
      blocks.push(
        <div className="delbot-structured-table-wrap" key={`table-${index}`}>
          <table className="delbot-structured-table">
            <thead>
              <tr>
                {header.map((cell, cellIndex) => (
                  <th key={`head-${cellIndex}`}>
                    {delbotInsightInline(cell)}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row, rowIndex) => (
                <tr key={`row-${rowIndex}`}>
                  {row.map((cell, cellIndex) => (
                    <td key={`cell-${rowIndex}-${cellIndex}`}>
                      {delbotInsightInline(cell)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>,
      );
      continue;
    }

    const heading = line.match(/^(#{2,4})\s+(.+)$/);
    if (heading) {
      const level = heading[1].length;
      const content = heading[2];
      blocks.push(
        level === 2 ? (
          <h2 key={`heading-${index}`}>{delbotInsightInline(content)}</h2>
        ) : (
          <h3 key={`heading-${index}`}>{delbotInsightInline(content)}</h3>
        ),
      );
      index += 1;
      continue;
    }

    const numbered = line.match(/^\d+[.)]\s+(.+)$/);
    if (numbered) {
      const items = [];
      while (index < lines.length) {
        const match = lines[index].trim().match(/^\d+[.)]\s+(.+)$/);
        if (!match) break;
        items.push(match[1]);
        index += 1;
      }
      blocks.push(
        <ol key={`ordered-${index}`}>
          {items.map((item, itemIndex) => (
            <li key={`ordered-item-${itemIndex}`}>
              {delbotInsightInline(item)}
            </li>
          ))}
        </ol>,
      );
      continue;
    }

    const bullet = line.match(/^[-*]\s+(.+)$/);
    if (bullet) {
      const items = [];
      while (index < lines.length) {
        const match = lines[index].trim().match(/^[-*]\s+(.+)$/);
        if (!match) break;
        items.push(match[1]);
        index += 1;
      }
      blocks.push(
        <ul key={`unordered-${index}`}>
          {items.map((item, itemIndex) => (
            <li key={`unordered-item-${itemIndex}`}>
              {delbotInsightInline(item)}
            </li>
          ))}
        </ul>,
      );
      continue;
    }

    const paragraph = [line];
    index += 1;
    while (index < lines.length) {
      const next = lines[index].trim();
      if (
        !next
        || /^(?:#{2,4})\s+/.test(next)
        || /^\d+[.)]\s+/.test(next)
        || /^[-*]\s+/.test(next)
        || (isTableRow(next)
          && index + 1 < lines.length
          && isTableSeparator(lines[index + 1]))
      ) {
        break;
      }
      paragraph.push(next);
      index += 1;
    }
    blocks.push(
      <p key={`paragraph-${index}`}>
        {delbotInsightInline(paragraph.join(" "))}
      </p>,
    );
  }

  return <div className="delbot-structured-answer">{blocks}</div>;
}

function DelbotInsightAnswerView({
  answer,
}: {
  answer: string;
}) {
  const lines = answer
    .replace(/^\s*svg\s*$/gim, "")
    .split("\n");

  return (
    <div className="delbot-insight-answer">
      {lines.map((rawLine, index) => {
        const line = rawLine.trim();

        if (!line) {
          return (
            <div
              aria-hidden="true"
              className="delbot-insight-space"
              key={`space-${index}`}
            />
          );
        }

        if (/^#{1,4}\s+/.test(line)) {
          return (
            <h3 key={`heading-${index}`}>
              {delbotInsightInline(
                line.replace(/^#{1,4}\s+/, ""),
              )}
            </h3>
          );
        }

        if (/^\*\*Ide\s+\d+\*\*$/i.test(line)) {
          return (
            <div
              className="delbot-insight-idea-heading"
              key={`idea-${index}`}
            >
              {line.replace(/\*/g, "")}
            </div>
          );
        }

        if (/^[-•]\s+/.test(line)) {
          return (
            <div
              className="delbot-insight-list-item"
              key={`list-${index}`}
            >
              <span />
              <p>
                {delbotInsightInline(
                  line.replace(/^[-•]\s+/, ""),
                )}
              </p>
            </div>
          );
        }

        const isResearchField =
          /^\*\*(Judul|Masalah|Research Gap|Metode|Metode Sistem yang Diusulkan|Rencana Evaluasi|Kontribusi|Keterbatasan|Sumber Pendukung|Temuan|Dataset|Evidence)\s*:/i.test(
            line,
          );

        return (
          <p
            className={
              isResearchField
                ? "delbot-insight-field"
                : "delbot-insight-paragraph"
            }
            key={`line-${index}`}
          >
            {delbotInsightInline(line)}
          </p>
        );
      })}
    </div>
  );
}


// DELBOT MVP friendly evidence presentation
function delbotFriendlyEvidenceType(value: string): string {
  const normalized = value
    .trim()
    .toLowerCase()
    .replace(/[\s-]+/g, "_");

  if (
    normalized.includes("fulltext")
    || normalized.includes("full_text")
    || normalized.includes("pdf")
    || normalized.includes("chunk")
  ) {
    return "Isi PDF";
  }

  if (
    normalized.includes("metadata_abstract")
    || normalized.includes("abstract")
  ) {
    return "Metadata/Abstrak";
  }

  if (normalized.includes("metadata")) {
    return "Metadata dokumen";
  }

  if (
    normalized.includes("repository")
    || normalized.includes("evidence")
  ) {
    return "Sumber repository";
  }

  return value.trim() || "Sumber repository";
}

function delbotFriendlyResearchAnswer(
  answer: string,
  evidence: DelbotInsightEvidence[],
): string {
  let friendlyAnswer = answer;

  evidence.forEach((source, index) => {
    const documentId = source.documentId.trim();

    if (
      !documentId
      || documentId === "Tidak tersedia"
    ) {
      return;
    }

    const escapedId = documentId.replace(
      /[.*+?^${}()|[\]\\]/g,
      "\\$&",
    );
    const sourceLabel = `Sumber ${index + 1}`;

    friendlyAnswer = friendlyAnswer
      .replace(
        new RegExp(
          `Evidence\\s+${escapedId}\\s+menjelaskan\\s*:`,
          "gi",
        ),
        `Berdasarkan ${sourceLabel}:`,
      )
      .replace(
        new RegExp(`Evidence\\s+${escapedId}`, "gi"),
        sourceLabel,
      )
      .replace(
        new RegExp(`\\[${escapedId}\\]`, "g"),
        `[${sourceLabel}]`,
      );
  });

  return friendlyAnswer
    .replace(
      /Evidence\s+123456789[-/]\d+\s+menjelaskan\s*:/gi,
      "Berdasarkan dokumen repository:",
    )
    .replace(
      /Evidence\s+123456789[-/]\d+/gi,
      "Dokumen repository",
    )
    .replace(
      /\[123456789[-/]\d+\]/g,
      "[Sumber repository]",
    )
    .replace(
      /\bmetadata_abstract\b/gi,
      "Metadata/Abstrak",
    )
    .replace(
      /\bmetadata_only\b/gi,
      "Metadata dokumen",
    );
}

function delbotInsightHasValue(
  value: string,
): boolean {
  const normalized = value.trim().toLowerCase();

  return Boolean(
    normalized
      && normalized !== "tidak dicantumkan"
      && normalized !== "tidak tersedia"
      && normalized !== "null"
      && normalized !== "none",
  );
}

function delbotInsightSafeRepositoryUrl(
  value: string,
): string {
  const candidate = value.trim();

  if (!candidate) {
    return "";
  }

  try {
    const parsed = new URL(candidate);

    if (
      parsed.protocol !== "http:"
      && parsed.protocol !== "https:"
    ) {
      return "";
    }

    return parsed.toString();
  } catch {
    return "";
  }
}

function delbotInsightConciseText(
  value: string,
  limit: number,
): string {
  const clean = value.replace(/\s+/g, " ").trim();

  if (clean.length <= limit) {
    return clean;
  }

  const shortened = clean
    .slice(0, limit)
    .replace(/\s+\S*$/, "")
    .trim();

  return `${shortened}…`;
}

function DelbotResearchInsightModal({
  message,
  onClose,
}: {
  message: unknown;
  onClose: () => void;
}) {
  const [selectedIndex, setSelectedIndex] = useState(0);

  // DELBOT UI contextual tabs 767916
  const [activeInsightTab, setActiveInsightTab] =
    useState<"answer" | "sources">("answer");

  useEffect(() => {
    setActiveInsightTab("answer");
  }, [message]);

  const [copied, setCopied] = useState(false);

  const answer = delbotInsightAnswer(message);
  const evidence = delbotInsightEvidence(message);
  const friendlyAnswer = delbotFriendlyResearchAnswer(
    answer,
    evidence,
  );
  const ideaCount = (
    friendlyAnswer.match(
      /(?:^|\n)\s*(?:#{1,4}\s*)?(?:\*\*)?Ide\s+[123]\b/gi,
    ) ?? []
  ).length;
  const selected = evidence[selectedIndex] ?? null;


  // DELBOT UI V3 repository document viewer V2
  const [pdfAccess, setPdfAccess] = useState({
    loading: false,
    available: false,
  });
  const [pdfViewerOpen, setPdfViewerOpen] = useState(false);

  useEffect(() => {
    const documentId = selected?.documentId?.trim();

    setPdfViewerOpen(false);

    if (
      !documentId
      || !/^\d+-\d+$/.test(documentId)
    ) {
      setPdfAccess({
        loading: false,
        available: false,
      });
      return;
    }

    const controller = new AbortController();

    setPdfAccess({
      loading: true,
      available: false,
    });

    fetch(
      `/api/chat/documents/${encodeURIComponent(documentId)}/pdf/status`,
      { signal: controller.signal },
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error("PDF status unavailable");
        }

        return response.json();
      })
      .then((payload) => {
        setPdfAccess({
          loading: false,
          available: payload?.available === true,
        });
      })
      .catch((error) => {
        if (error?.name === "AbortError") {
          return;
        }

        setPdfAccess({
          loading: false,
          available: false,
        });
      });

    return () => controller.abort();
  }, [selected?.documentId]);

  useEffect(() => {
    setSelectedIndex(0);
    setCopied(false);
  }, [message]);

  useEffect(() => {
    if (!message) {
      return undefined;
    }

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        onClose();
      }
    };

    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [message, onClose]);

  if (!message) {
    return null;
  }

  const copyAnswer = async () => {
    try {
      await navigator.clipboard.writeText(friendlyAnswer);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1600);
    } catch {
      setCopied(false);
    }
  };

  return (
    <div
      aria-label="Insight penelitian DELBot"
      aria-modal="true"
      className="delbot-insight-backdrop"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) {
          onClose();
        }
      }}
      role="dialog"
    >
      <div className="delbot-insight-modal">
        <header className="delbot-insight-header">
          <div className="delbot-insight-heading">
            <span className="delbot-insight-kicker">
              <i aria-hidden="true" />
              DELBot
            </span>

            <h2>Hasil penelusuran</h2>

            <p>
              Baca jawabannya, pindah antar sumber, dan buka repository
              hanya saat kamu membutuhkannya.
            </p>

            <div className="delbot-insight-header-meta">
              <span>{evidence.length} sumber relevan</span>
              {ideaCount > 0 ? (
                <span>{ideaCount} ide penelitian</span>
              ) : null}
            </div>
          </div>

          <div className="delbot-insight-actions">
            <button onClick={copyAnswer} type="button">
              {copied ? "Sudah disalin" : "Salin"}
            </button>
            <button
              className="is-primary"
              onClick={onClose}
              type="button"
            >
              Tutup
            </button>
          </div>
        </header>

        <nav
          aria-label="Navigasi hasil penelitian"
          className="delbot-insight-tabs"
        >
          <button
            aria-pressed={activeInsightTab === "answer"}
            className={
              activeInsightTab === "answer"
                ? "is-active"
                : ""
            }
            onClick={() => setActiveInsightTab("answer")}
            type="button"
          >
            Jawaban
          </button>

          <button
            aria-pressed={activeInsightTab === "sources"}
            className={
              activeInsightTab === "sources"
                ? "is-active"
                : ""
            }
            onClick={() => setActiveInsightTab("sources")}
            type="button"
          >
            Sumber
            <span>{evidence.length}</span>
          </button>
        </nav>


        <main
          className="delbot-insight-layout"
          data-active-tab={activeInsightTab}
        >
          <section className="delbot-insight-answer-panel">
            <div className="delbot-insight-panel-title">
              <div>
                <span>JAWABAN</span>
                <h3>Jawaban</h3>
              </div>
              <small>{evidence.length} sumber ditelusuri</small>
            </div>

            <div className="delbot-insight-scroll">
              <DelbotStructuredAnswerView answer={friendlyAnswer} />
            </div>
          </section>

          <aside className="delbot-insight-source-panel">
            <div className="delbot-insight-panel-title">
              <div>
                <span>REFERENSI</span>
                <h3>Sumber repository</h3>
              </div>
              <small>{evidence.length} dokumen</small>
            </div>

            {evidence.length > 0 ? (
              <>
                <div className="delbot-insight-source-list">
                  {evidence.map((source, index) => (
                    <button
                      className={
                        index === selectedIndex
                          ? "delbot-insight-source is-active"
                          : "delbot-insight-source"
                      }
                      key={source.key}
                      onClick={() => setSelectedIndex(index)}
                      type="button"
                    >
                      <b>{String(index + 1).padStart(2, "0")}</b>
                      <span>
                        <strong>{source.title}</strong>
                        <small>
                          {source.evidenceType}
                          {delbotInsightHasValue(source.year)
                            ? ` · ${source.year}`
                            : ""}
                          {delbotInsightHasValue(source.prodi)
                            ? ` · ${source.prodi}`
                            : ""}
                        </small>
                      </span>
                    </button>
                  ))}
                </div>

                {selected ? (
                  <article
                    className={
                      selected.isFulltext
                        ? "delbot-insight-source-detail is-fulltext"
                        : "delbot-insight-source-detail is-metadata"
                    }
                  >
                    {/* DELBOT MVP source explorer v2 render */}
                    <div className="delbot-insight-source-hero">
                      <div>
                        <span className="delbot-insight-type">
                          {selected.evidenceType}
                        </span>
                        <small>
                          Sumber {selectedIndex + 1} dari {evidence.length}
                        </small>
                      </div>
                      <span className="delbot-insight-source-status">
                        {selected.isFulltext
                          ? "Teks lengkap terhubung"
                          : "Metadata repository"}
                      </span>
                    </div>


                    <h4>{selected.title}</h4>

                    <div className="delbot-document-actions">
                      {pdfAccess.loading ? (
                        <span className="is-checking">
                          Memeriksa PDF…
                        </span>
                      ) : null}

                      {pdfAccess.available ? (
                        <>
                          <button
                            onClick={() => setPdfViewerOpen(true)}
                            type="button"
                          >
                            Visualisasikan PDF
                          </button>

                          <a
                            href={`/api/chat/documents/${encodeURIComponent(
                              selected.documentId,
                            )}/pdf?download=true`}
                          >
                            Unduh PDF
                          </a>
                        </>
                      ) : null}

                      {!pdfAccess.loading
                      && !pdfAccess.available
                      && selected.isFulltext ? (
                        <button
                          className="is-secondary"
                          onClick={() => setPdfViewerOpen(true)}
                          type="button"
                        >
                          Baca cuplikan
                        </button>
                      ) : null}
                    </div>

                    <dl className="delbot-insight-source-meta">
                      <div>
                        <dt>Penulis</dt>
                        <dd>{selected.author}</dd>
                      </div>
                      <div>
                        <dt>Tahun</dt>
                        <dd>{selected.year}</dd>
                      </div>
                      <div>
                        <dt>Program studi</dt>
                        <dd>{selected.prodi}</dd>
                      </div>
                      <div>
                        <dt>Kode repository</dt>
                        <dd>{selected.documentId}</dd>
                      </div>

                      {selected.isFulltext
                        && delbotInsightHasValue(selected.section) ? (
                          <div>
                            <dt>Bab atau bagian</dt>
                            <dd>{selected.section}</dd>
                          </div>
                        ) : null}

                      {selected.isFulltext
                        && delbotInsightHasValue(selected.page) ? (
                          <div>
                            <dt>Halaman</dt>
                            <dd>{selected.page}</dd>
                          </div>
                        ) : null}
                    </dl>

                    <div className="delbot-insight-excerpt">
                      <span>
                        {selected.isFulltext
                          ? "Ringkasan isi PDF"
                          : "Ringkasan metadata/abstrak"}
                      </span>
                      <p>
                        {delbotInsightConciseText(
                          selected.excerpt,
                          selected.isFulltext ? 1400 : 900,
                        )}
                      </p>
                    </div>

                    {delbotInsightSafeRepositoryUrl(selected.url) ? (
                      <a
                        className="delbot-insight-source-link"
                        href={delbotInsightSafeRepositoryUrl(
                          selected.url,
                        )}
                        rel="noreferrer"
                        target="_blank"
                      >
                        <span>Buka dokumen di repository</span>
                        <b>Open</b>
                      </a>
                    ) : null}

                    <p className="delbot-insight-note">
                      {selected.isFulltext
                        ? "Bagian dan halaman ditampilkan hanya ketika tersedia pada payload isi PDF."
                        : "Sumber ini berasal dari metadata atau abstrak. DELBot tidak menganggapnya sebagai isi lengkap PDF."}
                    </p>
                  </article>
                ) : null}
              </>
            ) : (
              <div className="delbot-insight-empty">
                <strong>Evidence relevan belum tersedia</strong>
                <p>
                  DELBot tidak menggunakan dokumen dari domain lain sebagai
                  sumber pendukung. Tambahkan dokumen relevan atau
                  perjelas topik penelitian.
                </p>
              </div>
            )}
          </aside>
        </main>

        {pdfViewerOpen && selected ? (
          <div
            aria-label="Pratinjau dokumen repository"
            aria-modal="true"
            className="delbot-document-viewer-backdrop"
            onMouseDown={(event) => {
              if (event.target === event.currentTarget) {
                setPdfViewerOpen(false);
              }
            }}
            role="dialog"
          >
            <section className="delbot-document-viewer">
              <header>
                <div>
                  <span>
                    {pdfAccess.available
                      ? "PDF REPOSITORY"
                      : "CUPLIKAN FULLTEXT"}
                  </span>
                  <h3>{selected.title}</h3>
                </div>

                <button
                  aria-label="Tutup pratinjau"
                  onClick={() => setPdfViewerOpen(false)}
                  type="button"
                >
                  Tutup
                </button>
              </header>

              <div className="delbot-document-viewer-body">
                {pdfAccess.available ? (
                  <iframe
                    src={`/api/chat/documents/${encodeURIComponent(
                      selected.documentId,
                    )}/pdf`}
                    title={`PDF ${selected.title}`}
                  />
                ) : (
                  <article className="delbot-document-text-preview">
                    <div>
                      {delbotInsightHasValue(selected.section) ? (
                        <span>{selected.section}</span>
                      ) : null}

                      {delbotInsightHasValue(selected.page) ? (
                        <span>Halaman {selected.page}</span>
                      ) : null}
                    </div>

                    <p>{selected.excerpt}</p>
                  </article>
                )}
              </div>

              <footer>
                <span>
                  {pdfAccess.available
                    ? "File asli dari repository."
                    : "Fulltext hasil parsing repository."}
                </span>

                {pdfAccess.available ? (
                  <a
                    href={`/api/chat/documents/${encodeURIComponent(
                      selected.documentId,
                    )}/pdf?download=true`}
                  >
                    Unduh PDF
                  </a>
                ) : null}
              </footer>
            </section>
          </div>
        ) : null}
      </div>
    </div>
  );
}


// DELBOT MVP compact research result card
function DelbotCompactResearchResultCard({
  message,
  onOpen,
}: {
  message: unknown;
  onOpen: () => void;
}) {
  const answer = delbotInsightAnswer(message);
  const evidence = delbotInsightEvidence(message);
  const friendlyAnswer = delbotFriendlyResearchAnswer(
    answer,
    evidence,
  );

  const ideaCount = (
    friendlyAnswer.match(
      /(?:^|\n)\s*(?:#{1,4}\s*)?(?:\*\*)?Ide\s+[123]\b/gi,
    ) ?? []
  ).length;

  const titleMatch = friendlyAnswer.match(
    /\*\*Judul:\*\*\s*([^\n]+)/i,
  );

  const headingMatch = friendlyAnswer.match(
    /^#{1,4}\s+([^\n]+)/m,
  );

  const resultTitle =
    titleMatch?.[1]?.trim()
    || headingMatch?.[1]?.trim()
    || (
      ideaCount > 0
        ? `${ideaCount} rekomendasi ide tugas akhir`
        : `${evidence.length} referensi yang relevan dengan pertanyaanmu`
    );

  const evidenceKinds = Array.from(
    new Set(
      evidence.map((source) => source.evidenceType),
    ),
  ).slice(0, 2);

  return (
    <article className="delbot-compact-research-card">
      <div className="delbot-compact-research-accent" />

      <div className="delbot-compact-research-body">
        <div className="delbot-compact-research-header">
          <div>
            <span>
              <i aria-hidden="true" />
              DELBot
            </span>

            <h3>
              {ideaCount > 0
                ? `${ideaCount} ide siap kamu eksplor`
                : `${evidence.length} referensi siap kamu eksplor`}
            </h3>
          </div>

          <div className="delbot-compact-research-status">
            <strong>{evidence.length}</strong>
            sumber
          </div>
        </div>

        <p className="delbot-compact-research-title">
          {resultTitle}
        </p>

        <div className="delbot-compact-research-meta">
          {ideaCount > 0 ? (
            <span>
              <strong>{ideaCount}</strong>
              ide penelitian
            </span>
          ) : null}

          {evidenceKinds.map((kind) => (
            <span key={kind}>{kind}</span>
          ))}
        </div>

        <div className="delbot-compact-research-footer">
          <p>
            Baca insight lengkap dan cek setiap sumbernya.
          </p>

          <button onClick={onOpen} type="button">
            Lihat insight
            <span aria-hidden="true">→</span>
          </button>
        </div>
      </div>
    </article>
  );
}

// DELBOT MVP main workspace UI V4
function delbotIsRequestError(
  message: unknown,
): boolean {
  const answer = delbotInsightAnswer(message);

  return (
    /permintaan belum berhasil diproses/i.test(answer)
    || /timeout of \d+ms exceeded/i.test(answer)
    || /request failed with status code/i.test(answer)
  );
}

function DelbotRequestError({
  onRetry,
}: {
  onRetry?: () => void;
}) {
  return (
    <article
      className="delbot-request-error"
      role="alert"
    >
      <div className="delbot-request-error-icon">
        <span />
      </div>

      <div className="delbot-request-error-copy">
        <span>RESPONS TERHENTI</span>
        <strong>Belum sempat menyelesaikan jawaban</strong>
        <p>
          Koneksi model membutuhkan waktu lebih lama. Kamu bisa
          mencoba kembali tanpa mengetik ulang pertanyaan.
        </p>
      </div>

      {onRetry ? (
        <button
          onClick={onRetry}
          type="button"
        >
          Coba lagi
          <span aria-hidden="true">↗</span>
        </button>
      ) : null}
    </article>
  );
}

export default function ConversationWorkspace() {
    const initialThread = useMemo(
        () => ensureActiveThread(),
        [],
    );

    const [
        thread,
        setThread,
    ] = useState<ConversationThread>(
        initialThread,
    );

    const [
        messages,
        setMessages,
    ] = useState<ConversationMessage[]>(
        initialThread.messages,
    );

  // DELBOT MVP research insight workspace state
  const [researchInsightMessage, setResearchInsightMessage] =
    useState<unknown>(null);

  // DELBOT UI V3: Research Insight opens only from its card.
  // This keeps everyday conversation and Q&A lightweight.


    const [
        loading,
        setLoading,
    ] = useState(false);

    const bottomRef =
        useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        const handleThreadSelection = (
            event: Event,
        ) => {
            const selectedId =
                (
                    event as CustomEvent<string>
                ).detail;

            const selected =
                loadConversationThreads().find(
                    (candidate) =>
                        candidate.id ===
                        selectedId,
                );

            if (!selected) {
                return;
            }

            setThread(selected);
            setMessages(selected.messages);
            setLoading(false);
        };

        window.addEventListener(
            THREAD_SELECTED_EVENT,
            handleThreadSelection,
        );

        return () => {
            window.removeEventListener(
                THREAD_SELECTED_EVENT,
                handleThreadSelection,
            );
        };
    }, []);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({
            behavior: "smooth",
            block: "end",
        });
    }, [messages, loading]);

    const persistMessages = (
        nextMessages: ConversationMessage[],
        nextSessionId = thread.sessionId,
    ) => {
        const nextThread =
            saveConversationThread({
                ...thread,
                sessionId: nextSessionId,
                title: conversationTitle(
                    nextMessages,
                ),
                messages: nextMessages,
            });

        setThread(nextThread);
        setMessages(nextThread.messages);
    };

    const handleSubmit = async (
        question: string,
    ) => {
        if (loading) {
            return;
        }

        const userMessage:
            ConversationMessage = {
                id: messageId("user"),
                role: "user",
                content: question,
                createdAt: Date.now(),
            };

        const pendingMessages = [
            ...messages,
            userMessage,
        ];

        persistMessages(pendingMessages);
        setLoading(true);

        try {
            const response =
                await researchAnswer(
                    question,
                    thread.sessionId,
                );

            const payload = response.data;

            const assistantMessage:
                ConversationMessage = {
                    id: messageId("assistant"),
                    role: "assistant",
                    content:
                        String(
                            payload.answer ?? "",
                        ).trim() ||
                        "DELBot tidak menerima jawaban yang dapat ditampilkan.",
                    citations: Array.isArray(
                        payload.citations,
                    )
                        ? (
                              payload.citations as unknown as CitationRecord[]
                          )
                        : [],
                    createdAt: Date.now(),
                };

            persistMessages(
                [
                    ...pendingMessages,
                    assistantMessage,
                ],
                payload.session_id ||
                    thread.sessionId,
            );
        } catch (error) {
            const message =
                error instanceof Error
                    ? error.message
                    : "Unknown request error";

            const errorMessage:
                ConversationMessage = {
                    id: messageId("assistant"),
                    role: "assistant",
                    content:
                        "Permintaan belum berhasil diproses. " +
                        `Silakan coba lagi. (${message})`,
                    citations: [],
                    createdAt: Date.now(),
                };

            persistMessages([
                ...pendingMessages,
                errorMessage,
            ]);
        } finally {
            setLoading(false);
        }
    };

    const empty = messages.length === 0;

    return (
        <section className="delbot-conversation-workspace">
            <header className="delbot-workspace-topbar">
                <div className="delbot-workspace-heading">
                    <span className="delbot-workspace-signal">
                        <i />
                    </span>

                    <div>
                        <small>DELBOT</small>
                        <strong>Temukan sumber. Susun langkah.</strong>
                        <p>
                            Telusuri repository dan lanjutkan penelitianmu.
                        </p>
                    </div>
                </div>

                <div className="delbot-workspace-mode">
                    <span></span>
                    <i />
                </div>
            </header>

      {/* DELBOT MVP research insight workspace render */}
      <DelbotResearchInsightModal
        message={researchInsightMessage}
        onClose={() => setResearchInsightMessage(null)}
      />

            <div className="delbot-conversation-stage">
                <div
                    className={[
                        "delbot-message-viewport",
                        empty
                            ? "delbot-message-viewport-empty"
                            : "",
                    ]
                        .filter(Boolean)
                        .join(" ")}
                >
                    {empty ? (
                        <div className="delbot-empty-state">
                            <div
                                className="delbot-empty-orbit"
                                aria-hidden="true"
                            >
                                <span />
                                <i />
                                <b>D</b>
                            </div>

                            <span className="delbot-empty-eyebrow">
                                YOUR DELBOT
                            </span>

                            <h1>
                                Apa yang ingin kamu teliti?
                            </h1>

                            <p>
                                Tanya apa saja, telusuri repository,
                                lalu ubah evidence menjadi insight
                                yang bisa kamu kerjakan.
                            </p>

                            <div className="delbot-empty-capabilities">
                                <span>Cari sumber</span>
                                <span>Bedah penelitian</span>
                                <span>Temukan gap</span>
                                <span>Buka PDF</span>
                            </div>
                        </div>
                    ) : (
                        <div className="delbot-message-list">
                            {/* DELBOT MVP compact research message branch */}
                            {messages.map((message, index) => {
                                if (
                                    delbotIsResearchResult(message)
                                ) {
                                    return (
                                        <DelbotCompactResearchResultCard
                                            key={message.id}
                                            message={message}
                                            onOpen={() =>
                                                setResearchInsightMessage(
                                                    message,
                                                )
                                            }
                                        />
                                    );
                                }

                                if (
                                    delbotIsRequestError(message)
                                ) {
                                    const retryText =
                                        index > 0
                                            ? delbotInsightAnswer(
                                                  messages[index - 1],
                                              )
                                            : "";

                                    return (
                                        <DelbotRequestError
                                            key={message.id}
                                            onRetry={
                                                retryText
                                                    ? () => {
                                                          void handleSubmit(
                                                              retryText,
                                                          );
                                                      }
                                                    : undefined
                                            }
                                        />
                                    );
                                }

                                return (
                                    <Bubble
                                        key={message.id}
                                        message={message}
                                    />
                                );
                            })}

                            {loading ? (
                                <div
                                    className="delbot-thinking"
                                    role="status"
                                    aria-live="polite"
                                >
                                    <div className="delbot-thinking-mark">
                                        <Bot size={16} />
                                    </div>

                                    <div className="delbot-thinking-copy">
                                        <strong>
                                            Sedang meracik jawaban
                                        </strong>
                                        <span>
                                            Menelusuri evidence dan
                                            menyusun insight…
                                        </span>
                                    </div>

                                    <div
                                        className="delbot-thinking-dots"
                                        aria-hidden="true"
                                    >
                                        <i />
                                        <i />
                                        <i />
                                    </div>
                                </div>
                            ) : null}

                            <div ref={bottomRef} />
                        </div>
                    )}
                </div>

                <ResearchInputDock
                    loading={loading}
                    empty={empty}
                    onSubmit={handleSubmit}
                />
            </div>
        </section>
    );
}
