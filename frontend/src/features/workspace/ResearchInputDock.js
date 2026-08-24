import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useRef, useState, } from "react";
import { ArrowUp, } from "lucide-react";
const actions = [
    {
        label: "Review literature",
        prompt: "Tinjau literatur paling relevan dalam repositori. Sintesis tema utama, metode, temuan, perbedaan hasil, keterbatasan, dan sumber yang digunakan.",
    },
    {
        label: "Compare studies",
        prompt: "Bandingkan studi paling relevan dalam repositori berdasarkan masalah, dataset, metode, metrik evaluasi, hasil, keterbatasan, dan sumber yang digunakan.",
    },
    {
        label: "Find a gap",
        prompt: "Identifikasi research gap yang benar-benar didukung oleh koleksi. Jelaskan evidence, keterbatasan studi terdahulu, aspek yang belum dibahas, dan peluang penelitian.",
    },
    {
        label: "Develop an idea",
        prompt: "Kembangkan beberapa thesis ideas dari evidence dan research gap dalam koleksi. Untuk setiap ide jelaskan masalah, gap, arah metode, kontribusi yang diharapkan, dan sumber pendukung.",
    },
];
export default function ResearchInputDock({ loading, onSubmit, empty = false, }) {
    const [question, setQuestion] = useState("");
    const textareaRef = useRef(null);
    const resizeTextarea = () => {
        const textarea = textareaRef.current;
        if (!textarea) {
            return;
        }
        textarea.style.height = "auto";
        textarea.style.height =
            `${Math.min(textarea.scrollHeight, 152)}px`;
    };
    const submit = async () => {
        const value = question.trim();
        if (!value || loading) {
            return;
        }
        setQuestion("");
        if (textareaRef.current) {
            textareaRef.current.style.height =
                "auto";
        }
        await onSubmit(value);
    };
    return (_jsx("div", { className: [
            "delbot-composer-zone",
            empty
                ? "delbot-composer-zone-empty"
                : "",
        ]
            .filter(Boolean)
            .join(" "), children: _jsxs("div", { className: "delbot-composer-shell", children: [_jsxs("div", { className: "delbot-composer-row", children: [_jsx("textarea", { ref: textareaRef, value: question, rows: 1, placeholder: empty
                                ? "Ask DELBot anything…"
                                : "Continue the conversation…", "aria-label": "Message DELBot", onChange: (event) => {
                                setQuestion(event.target.value);
                                resizeTextarea();
                            }, onKeyDown: (event) => {
                                if (event.key === "Enter" &&
                                    !event.shiftKey) {
                                    event.preventDefault();
                                    void submit();
                                }
                            } }), _jsx("button", { type: "button", className: "delbot-send-button", disabled: loading ||
                                question.trim().length === 0, onClick: () => {
                                void submit();
                            }, "aria-label": loading
                                ? "DELBot is responding"
                                : "Send message", children: _jsx(ArrowUp, { size: 18 }) })] }), _jsxs("div", { className: "delbot-composer-meta", children: [_jsx("div", { className: "delbot-research-actions", children: actions.map((action) => (_jsx("button", { type: "button", onClick: () => {
                                    setQuestion(action.prompt);
                                    requestAnimationFrame(() => {
                                        resizeTextarea();
                                        textareaRef.current?.focus();
                                    });
                                }, children: action.label }, action.label))) }), _jsx("span", { className: "delbot-key-hint", children: "Shift + Enter for new line" })] })] }) }));
}
