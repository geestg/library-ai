import { useState } from "react";
import {
    Search,
    Loader2,
    FileText,
} from "lucide-react";
import { researchAnswer } from "../../api/research";

type Citation = {
    document_id: string;
    source: string;
    section: string;
    page_start?: number;
    page_end?: number;
};

type SearchResponse = {
    answer: string;
    citations: Citation[];
};

export default function SearchPage() {

    const [query, setQuery] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [result, setResult] = useState<SearchResponse | null>(null);

    async function search() {

        if (!query.trim()) {
            setError("Query is required.");
            return;
        }

        setLoading(true);
        setError("");
        setResult(null);

        try {

            const response = await researchAnswer(query);

            setResult(response.data);

        } catch {

            setError("Search failed.");

        } finally {

            setLoading(false);

        }

    }

    const card: React.CSSProperties = {
        background: "#fff",
        border: "1px solid #e5e7eb",
        borderRadius: 12,
        padding: 24,
        boxShadow: "0 1px 4px rgba(0,0,0,.05)",
    };

    return (

        <div>

            <div
                style={{
                    display:"flex",
                    alignItems:"center",
                    gap:12,
                    marginBottom:24,
                }}
            >
                <Search size={30}/>
                <div>
                    <h1 style={{margin:0}}>
                        Semantic Search
                    </h1>
                    <p
                        style={{
                            marginTop:6,
                            color:"#6b7280",
                        }}
                    >
                        Search repository using existing research pipeline.
                    </p>
                </div>
            </div>

            <div style={card}>

                <textarea
                    rows={4}
                    value={query}
                    onChange={(e)=>setQuery(e.target.value)}
                    placeholder="Search repository..."
                    style={{
                        width:"100%",
                        padding:12,
                        boxSizing:"border-box",
                        resize:"vertical",
                    }}
                />

                <button
                    onClick={search}
                    disabled={loading}
                    style={{
                        marginTop:16,
                        padding:"10px 18px",
                        cursor:"pointer",
                        display:"flex",
                        alignItems:"center",
                        gap:8,
                    }}
                >
                    {loading && <Loader2 size={16}/>}
                    {loading ? "Searching..." : "Search"}
                </button>

                {error && (

                    <div
                        style={{
                            marginTop:16,
                            color:"#dc2626",
                        }}
                    >
                        {error}
                    </div>

                )}

            </div>

            {result && (

                <div
                    style={{
                        ...card,
                        marginTop:24,
                    }}
                >

                    <h2 style={{marginTop:0}}>
                        Answer
                    </h2>

                    <div
                        style={{
                            whiteSpace:"pre-wrap",
                        }}
                    >
                        {result.answer}
                    </div>

                    <h2
                        style={{
                            marginTop:28,
                        }}
                    >
                        Citations
                    </h2>

                    {result.citations.map((c,index)=>(

                        <div
                            key={index}
                            style={{
                                borderTop:
                                    index===0
                                    ? "none"
                                    : "1px solid #eee",
                                padding:"12px 0",
                                display:"flex",
                                gap:10,
                            }}
                        >

                            <FileText
                                size={18}
                                style={{marginTop:2}}
                            />

                            <div>

                                <strong>
                                    {c.document_id}
                                </strong>

                                <div>
                                    {c.section}
                                </div>

                                <div
                                    style={{
                                        color:"#6b7280",
                                        fontSize:13,
                                    }}
                                >
                                    Page {c.page_start ?? "-"}
                                    {c.page_end
                                        ? ` - ${c.page_end}`
                                        : ""}
                                </div>

                            </div>

                        </div>

                    ))}

                </div>

            )}

        </div>

    );

}
