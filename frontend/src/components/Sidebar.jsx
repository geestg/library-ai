import { BrainCircuit } from "lucide-react";

export default function Sidebar() {

  return (

    <aside className="modern-sidebar">

      {/* ============================= */}
      {/* BRAND */}
      {/* ============================= */}

      <div className="sidebar-top">

        <div className="sidebar-logo">

          <div className="logo-icon">

            <BrainCircuit size={22} />

          </div>

          <div>

            <h2>

              DELBot

            </h2>

            <span>

              Academic Research Intelligence

            </span>

          </div>

        </div>

      </div>

    </aside>

  );

}