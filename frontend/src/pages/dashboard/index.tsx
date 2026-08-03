import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";

import {
    Sparkles,
    BrainCircuit,
    FolderOpen,
    Search,
    Files,
    Clock3,
    BookOpen,
    SendHorizonal,
    ChevronRight,
    Loader2,
    Trash2,
} from "lucide-react";

import { repositoryExplorer } from "../../api/repository";
import { researchAnswer } from "../../api/research";

type Summary = {
    total: number;
    pdf_available: number;
    pdf_missing: number;
};

type Citation = {
    document_id: string;
    source: string;
    section: string;
    page_start?: number;
    page_end?: number;
};

type ResearchResponse = {
    answer: string;
    citations: Citation[];
};

type Message = {
    role: "user" | "assistant";
    content: string;
};

type WorkspaceSession = {
    id: string;
    title: string;
    created_at: string;
    updated_at: string;
    messages: Message[];
    result: ResearchResponse | null;
};

const WORKSPACE_STORAGE = "workspace_sessions";
const ACTIVE_WORKSPACE = "active_workspace";


const STORAGE_KEY = "delbot_workspace";

const STREAM_DELAY = 8;


export default function DashboardPage() {

    const conversationRef = useRef<HTMLDivElement>(null);

    const [loadingRepository, setLoadingRepository] = useState(true);
    const [loadingResearch, setLoadingResearch] = useState(false);

    const [prompt, setPrompt] = useState("");
    const [messages, setMessages] = useState<Message[]>([]);

    const [workspaceSessions, setWorkspaceSessions] =
        useState<WorkspaceSession[]>([]);

    const [activeWorkspaceId, setActiveWorkspaceId] =
        useState("");


    const [result, setResult] = useState<ResearchResponse | null>(null);

    const [summary, setSummary] = useState<Summary>({
        total: 0,
        pdf_available: 0,
        pdf_missing: 0,
    });
const id = Date.now().toString();

        const session = {
            id: crypto.randomUUID(),
            title: "New Conversation",
            preview: "",
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            messages: [],
            result: null,
        };

        setWorkspaceSessions((prev: WorkspaceSession[]) => [
            session,
            ...prev,
        ]);

        setActiveWorkspaceId(id);

        setMessages([]);
        setResult(null);
        setPrompt("");

    }

    

    
function switchWorkspace(id: string) {

        setActiveWorkspaceId(id);

}




    function renameWorkspace(id: string) {

        const name = window.prompt("Conversation title");

        if (!name) {
            return;
        }

        setWorkspaceSessions(prev =>
            prev.map(item =>
                item.id === id
                    ? {
                        ...item,
                        title: name,
                    }
                    : item
            )
        );

    }

    function deleteWorkspace(id: string) {

        if (!window.confirm("Delete conversation?")) {
            return;
        }

        const next = workspaceSessions.filter(
            item => item.id !== id
        );

        setWorkspaceSessions(next);

        if (activeWorkspaceId === id) {

            if (next.length > 0) {
            setActiveWorkspaceId(next[0].id);
        }

        }

    }



    

    return (

        <div
            style={{
                padding: 32,
            }}
        >

            <div
                style={{
                    background:"#ffffff",
                    border:"1px solid #e5e7eb",
                    borderRadius:16,
                    padding:24,
                }}
            >

                <h1
                    style={{
                        margin:0,
                        fontSize:32,
                    }}
                >
                    AI Research Workspace
                </h1>

                <p
                    style={{
                        color:"#64748b",
                        marginTop:12,
                        lineHeight:1.8,
                    }}
                >
                    Dashboard recovery completed.
                    Workspace will be restored gradually.
                </p>

            </div>

        </div>

    );

}
