import { useState } from "react";
import TabNav from "./components/TabNav.jsx";
import ChatTab from "./components/ChatTab.jsx";
import ClauseTab from "./components/ClauseTab.jsx";
import RiskTab from "./components/RiskTab.jsx";
import AgentTab from "./components/AgentTab.jsx";

const TAB_COMPONENTS = {
  chat: ChatTab,
  clause: ClauseTab,
  risk: RiskTab,
  agent: AgentTab,
};

export default function App() {
  const [active, setActive] = useState("chat");
  const ActiveTab = TAB_COMPONENTS[active];

  return (
    <div className="min-h-screen bg-paper">
      <header className="border-b border-line">
        <div className="px-6 sm:px-10 pt-8 pb-2">
          <p className="font-mono text-[11px] tracking-[0.2em] uppercase text-ink/40 mb-2">
            Indian Legal Reference &amp; Contract Analysis
          </p>
          <h1 className="font-serif text-3xl sm:text-4xl text-ink tracking-tight">
            VerdíQ
          </h1>
        </div>
        <TabNav active={active} onChange={setActive} />
      </header>

      <main className="bg-parchment border-b border-line min-h-[70vh]">
        <div className="px-6 sm:px-10 py-10">
          <ActiveTab />
        </div>
      </main>

      <footer className="px-6 sm:px-10 py-4">
        <p className="font-sans text-xs text-ink/40">
          Educational information only — not a substitute for advice from a
          qualified lawyer. 
        </p>
        <p className="font-sans text-ink/60">
          Developed by Maanya Gupta
        </p>
      </footer>
    </div>
  );
}
