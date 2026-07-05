import { useRef, useState } from "react";
import { extractClauses } from "../api.js";
import {
  Card,
  SectionLabel,
  PrimaryButton,
  ErrorBanner,
  LoadingSeal,
  MarkdownBlock,
} from "./Shared.jsx";

const CLAUSE_LABELS = {
  termination_clause: "Termination",
  payment_clause: "Payment",
  arbitration_clause: "Arbitration",
  confidentiality_clause: "Confidentiality",
  governing_law_clause: "Governing Law",
};

export default function ClauseTab() {
  const [file, setFile] = useState(null);
  const [clauses, setClauses] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const inputRef = useRef(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setError(null);
    setClauses(null);
    try {
      const res = await extractClauses(file);
      setClauses(res.clauses);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleFileChange(e) {
    const f = e.target.files?.[0];
    if (f) setFile(f);
  }

  return (
    <div className="max-w-2xl">
      <SectionLabel>Upload a contract</SectionLabel>
      <h2 className="font-serif text-2xl text-foreground mb-1">Clause Extraction</h2>
      <p className="text-muted-foreground font-sans text-sm mb-6">
        Pulls termination, payment, arbitration, confidentiality, and
        governing-law clauses from a contract PDF.
      </p>

      <form onSubmit={handleSubmit} className="mb-6">
        <div
          onClick={() => inputRef.current?.click()}
          className="focus-ring cursor-pointer border border-dashed border-border rounded-md bg-white px-6 py-8 text-center hover:border-primary transition-colors"
        >
          <input
            ref={inputRef}
            type="file"
            accept="application/pdf"
            onChange={handleFileChange}
            className="hidden"
          />
          <p className="font-sans text-sm text-brand-black/70">
            {file ? (
              <span className="font-medium text-brand-black">{file.name}</span>
            ) : (
              <>
                <span className="text-primary font-medium">
                  Choose a PDF
                </span>{" "}
                or drop it here
              </>
            )}
          </p>
        </div>
        <div className="mt-3">
          <PrimaryButton type="submit" disabled={loading || !file}>
            {loading ? "Reading contract…" : "Extract Clauses"}
          </PrimaryButton>
        </div>
      </form>

      {loading && (
        <LoadingSeal label="Parsing the document and identifying clauses…" />
      )}
      <ErrorBanner message={error} />

      {clauses && (
        <Card>
          <SectionLabel>Extracted Clauses</SectionLabel>
          <dl className="divide-y divide-border">
            {Object.entries(clauses).map(([key, value]) => (
              <div key={key} className="py-3 first:pt-0 last:pb-0">
                <dt className="font-sans text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-1">
                  {CLAUSE_LABELS[key] || key}
                </dt>
                <dd>
                  {value ? (
                    <MarkdownBlock>{value}</MarkdownBlock>
                  ) : (
                    <span className="font-sans text-sm text-muted-foreground italic">
                      Not found in this document
                    </span>
                  )}
                </dd>
              </div>
            ))}
          </dl>
        </Card>
      )}
    </div>
  );
}