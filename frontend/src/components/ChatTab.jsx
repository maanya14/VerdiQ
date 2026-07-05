import { useState } from "react";
import { askChat } from "../api.js";
import {
  Card,
  SectionLabel,
  PrimaryButton,
  ErrorBanner,
  LoadingSeal,
  MarkdownBlock,
} from "./Shared.jsx";

export default function ChatTab() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!question.trim()) return;
    setLoading(true);
    setError(null);
    setAnswer(null);
    try {
      const res = await askChat(question.trim());
      setAnswer(res.answer);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-2xl">
      <SectionLabel>Ask a legal question</SectionLabel>
      <h2 className="font-serif text-2xl text-foreground mb-1">General Counsel</h2>
      <p className="text-muted-foreground font-sans text-sm mb-6">
        Answered against the indexed Indian legal reference library.
      </p>

      <form onSubmit={handleSubmit} className="mb-6">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="e.g. What notice period is required to terminate a residential lease?"
          rows={3}
          className="focus-ring w-full border border-border rounded-md bg-white px-4 py-3 font-sans text-sm text-brand-black placeholder:text-brand-black/40 resize-none"
        />
        <div className="mt-3">
          <PrimaryButton type="submit" disabled={loading || !question.trim()}>
            {loading ? "Consulting the library…" : "Ask"}
          </PrimaryButton>
        </div>
      </form>

      {loading && <LoadingSeal label="Retrieving relevant statutes and drafting an answer…" />}
      <ErrorBanner message={error} />

      {answer && (
        <Card>
          <SectionLabel>Answer</SectionLabel>
          <MarkdownBlock>{answer}</MarkdownBlock>
        </Card>
      )}
    </div>
  );
}