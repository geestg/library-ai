import { BookOpen, MessageSquare, Search } from "lucide-react";

export default function Sidebar() {

  return (
    <div className="sidebar">

      <div className="logo">
        Library AI
      </div>

      <div className="menu">

        <button>
          <MessageSquare size={18} />
          Chat
        </button>

        <button>
          <Search size={18} />
          Search
        </button>

        <button>
          <BookOpen size={18} />
          Research
        </button>

      </div>

    </div>
  );
}