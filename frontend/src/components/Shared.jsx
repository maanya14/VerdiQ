export function Card({ children, className = "" }) {
  return (
    <div
      className={`bg-white border border-line rounded-lg p-6 sm:p-8 ${className}`}
    >
      {children}
    </div>
  );
}

export function SectionLabel({ children }) {
  return (
    <p className="font-mono text-[11px] tracking-[0.15em] uppercase text-brass mb-2">
      {children}
    </p>
  );
}

export function PrimaryButton({ children, disabled, ...props }) {
  return (
    <button
      disabled={disabled}
      className="focus-ring inline-flex items-center gap-2 bg-burgundy hover:bg-burgundy-dark disabled:bg-ink/20 disabled:cursor-not-allowed text-paper font-sans text-sm font-medium px-5 py-2.5 rounded-md transition-colors"
      {...props}
    >
      {children}
    </button>
  );
}

export function ErrorBanner({ message }) {
  if (!message) return null;
  return (
    <div className="border border-burgundy/30 bg-burgundy/[0.06] text-burgundy-dark text-sm rounded-md px-4 py-3 font-sans">
      <span className="font-semibold">Unable to complete request. </span>
      {message}
    </div>
  );
}

export function LoadingSeal({ label }) {
  return (
    <div className="flex items-center gap-3 text-ink/50 font-sans text-sm py-2">
      <span className="relative flex h-3 w-3">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brass opacity-60" />
        <span className="relative inline-flex rounded-full h-3 w-3 bg-brass" />
      </span>
      {label}
    </div>
  );
}
