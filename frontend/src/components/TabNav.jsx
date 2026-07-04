const TABS = [
  { id: "chat", numeral: "I", label: "General Counsel" },
  { id: "clause", numeral: "II", label: "Clause Extraction" },
  { id: "risk", numeral: "III", label: "Risk Assessment" },
  { id: "agent", numeral: "IV", label: "Full Case Review" },
];

export default function TabNav({ active, onChange }) {
  return (
    <div className="flex items-end gap-1 px-6 sm:px-10 pt-6" role="tablist">
      {TABS.map((tab) => {
        const isActive = tab.id === active;
        return (
          <button
            key={tab.id}
            role="tab"
            aria-selected={isActive}
            onClick={() => onChange(tab.id)}
            className={[
              "focus-ring group relative flex items-center gap-2 px-4 sm:px-5 py-3 rounded-t-lg border border-b-0 transition-colors",
              isActive
                ? "bg-brand-gold border-brand-gold text-brand-black shadow-md"
                : "bg-transparent border-transparent text-foreground/70 hover:text-foreground hover:bg-white/5"
            ].join(" ")}
          >
            <span
              className={[
                "font-mono text-[11px] tracking-wider",
                isActive ? "text-brand-black" : "text-brand-gold/70",
              ].join(" ")}
            >
              {tab.numeral}
            </span>
            <span className="font-sans text-sm font-medium whitespace-nowrap">
              {tab.label}
            </span>
            {isActive && (
              <span className="absolute -bottom-px left-4 right-4 h-px bg-parchment" />
            )}
          </button>
        );
      })}
    </div>
  );
}
