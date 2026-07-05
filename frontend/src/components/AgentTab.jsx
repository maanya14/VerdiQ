import { useState } from "react";
import { askAgent } from "../api.js";
import {
  Card,
  SectionLabel,
  PrimaryButton,
  ErrorBanner,
  LoadingSeal,
  MarkdownBlock,
} from "./Shared.jsx";

export default function AgentTab() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!question.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await askAgent(question.trim());
      setResult(res.result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-2xl">
      <SectionLabel>Full case review</SectionLabel>
      <h2 className="font-serif text-2xl text-foreground mb-1">Full Case Review</h2>
      <p className="text-muted-foreground font-sans text-sm mb-6">
        Runs the clause, risk, and advisory agents in sequence for a complete
        report. Slower than the other tabs — expect it to take a while.
      </p>

      <form onSubmit={handleSubmit} className="mb-6">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="e.g. Review the risks in a standard residential lease termination clause."
          rows={3}
          className="focus-ring w-full border border-border rounded-md bg-white px-4 py-3 font-sans text-sm text-brand-black placeholder:text-brand-black/40 resize-none"
        />
        <div className="mt-3">
          <PrimaryButton type="submit" disabled={loading || !question.trim()}>
            {loading ? "Convening counsel…" : "Request Full Review"}
          </PrimaryButton>
        </div>
      </form>

      {loading && (
        <LoadingSeal label="Clause, risk, and advisory agents are working through the file…" />
      )}
      <ErrorBanner message={error} />

      {result && (
        <Card>
          <SectionLabel>Final Report</SectionLabel>
          <MarkdownBlock>{result}</MarkdownBlock>
        </Card>
      )}
    </div>
  );
}