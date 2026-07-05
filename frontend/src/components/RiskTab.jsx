import { useState } from "react";
import { analyzeRisk } from "../api.js";
import {
  Card,
  SectionLabel,
  PrimaryButton,
  ErrorBanner,
  LoadingSeal,
  MarkdownBlock,
} from "./Shared.jsx";

const RISK_COLORS = {
  low: "bg-emerald-50 text-emerald-700 border-emerald-200",
  medium: "bg-amber-50 text-amber-700 border-amber-200",
  high: "bg-red-950/40 text-red-300 border-red-900/50",
};

function riskBadgeClass(level) {
  const key = (level || "").toString().toLowerCase();
  return RISK_COLORS[key] || "bg-muted text-muted-foreground border-border";
}

export default function RiskTab() {
  const [clause, setClause] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!clause.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await analyzeRisk(clause.trim());
      setResult(res.analysis);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  // The backend returns either structured JSON ({risk_level, explanation,
  // legal_citation, ...}) or, if the model didn't return clean JSON, a
  // { raw_response } fallback.
  const isStructured = result && !("raw_response" in result);

  return (
    <div className="max-w-2xl">
      <SectionLabel>Paste a clause</SectionLabel>
      <h2 className="font-serif text-2xl text-foreground mb-1">Risk Assessment</h2>
      <p className="text-muted-foreground font-sans text-sm mb-6">
        Weighs a single clause against the indexed statute library and flags
        its risk level.
      </p>

      <form onSubmit={handleSubmit} className="mb-6">
        <textarea
          value={clause}
          onChange={(e) => setClause(e.target.value)}
          placeholder="e.g. Landlord may terminate tenancy without notice and remove tenant."
          rows={4}
          className="focus-ring w-full border border-border rounded-md bg-white px-4 py-3 font-sans text-sm text-brand-black placeholder:text-brand-black/40 resize-none"
        />
        <div className="mt-3">
          <PrimaryButton type="submit" disabled={loading || !clause.trim()}>
            {loading ? "Weighing the clause…" : "Assess Risk"}
          </PrimaryButton>
        </div>
      </form>

      {loading && (
        <LoadingSeal label="Cross-referencing applicable law…" />
      )}
      <ErrorBanner message={error} />

      {result && (
        <Card>
          {isStructured ? (
            <div className="divide-y divide-border">
              {result.risk_level && (
                <div className="pb-4">
                  <SectionLabel>Risk Level</SectionLabel>
                  <span
                    className={`inline-block border text-xs font-semibold uppercase tracking-wide px-3 py-1 rounded-full font-sans ${riskBadgeClass(
                      result.risk_level
                    )}`}
                  >
                    {result.risk_level}
                  </span>
                </div>
              )}
              {result.explanation && (
                <div className="py-4">
                  <SectionLabel>Explanation</SectionLabel>
                  <MarkdownBlock>{result.explanation}</MarkdownBlock>
                </div>
              )}
              {result.legal_citation && (
                <div className="pt-4">
                  <SectionLabel>Legal Citation</SectionLabel>
                  <p className="font-mono text-sm text-foreground/80">
                    {result.legal_citation}
                  </p>
                </div>
              )}
              {!result.risk_level &&
                !result.explanation &&
                !result.legal_citation && (
                  <pre className="font-mono text-xs text-foreground/70 whitespace-pre-wrap">
                    {JSON.stringify(result, null, 2)}
                  </pre>
                )}
            </div>
          ) : (
            <div>
              <SectionLabel>Analysis</SectionLabel>
              <MarkdownBlock>{result.raw_response}</MarkdownBlock>
            </div>
          )}
        </Card>
      )}
    </div>
  );
}