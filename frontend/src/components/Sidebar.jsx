import {
  BrainCircuit,
} from "lucide-react";

export default function Sidebar() {

  return (

    <aside className="modern-sidebar">

      <div className="sidebar-top">

        <div className="sidebar-logo">

          <div className="logo-icon">

            <BrainCircuit
              size={22}
              strokeWidth={2}
            />

          </div>

          <div className="sidebar-brand-copy">

            <h2>
              DELBot
            </h2>

            <span>
              Academic Research
              <br />
              Intelligence
            </span>

          </div>

        </div>

      </div>

    </aside>

  );

}