export function Card({ children, className = "" }) {
  return (
    <div
      className={`bg-card border border-border rounded-xl p-6 sm:p-8 shadow-lg ${className}`}
    >
      {children}
    </div>
  );
}

export function SectionLabel({ children }) {
  return (
    <p className="font-mono text-[11px] tracking-[0.18em] uppercase text-primary mb-2">
      {children}
    </p>
  );
}

export function PrimaryButton({ children, disabled, ...props }) {
  return (
    <button
      disabled={disabled}
      className="
        focus-ring
        inline-flex
        items-center
        gap-2

        bg-primary
        text-primary-foreground

        hover:brightness-110
        hover:shadow-lg

        disabled:bg-secondary
        disabled:text-foreground/40
        disabled:cursor-not-allowed

        font-sans
        text-sm
        font-medium

        px-5
        py-2.5

        rounded-lg

        transition-all
        duration-200
        "
    >
      {children}
    </button>
  );
}

export function ErrorBanner({ message }) {
  if (!message) return null;
  return (
    <div className="
      border
      border-red-800

      bg-red-950/30

      text-red-300

      rounded-lg

      px-4
      py-3

      font-sans
      text-sm
      "
    >
      <span className="font-semibold">Unable to complete request. </span>
      {message}
    </div>
  );
}

export function LoadingSeal({ label }) {
  return (
    <div className="flex items-center gap-3 text-foreground/60 font-sans text-sm py-2">
      <span className="relative flex h-3 w-3">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-60" />
        <span className="relative inline-flex rounded-full h-3 w-3 bg-primary" />
      </span>
      {label}
    </div>
  );
}
