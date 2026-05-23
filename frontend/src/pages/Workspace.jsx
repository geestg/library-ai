import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";
import SearchPanel from "../components/SearchPanel";

export default function Workspace() {

  return (
    <div className="app-container">

      <Sidebar />

      <ChatWindow />

      <SearchPanel />

    </div>
  );
}