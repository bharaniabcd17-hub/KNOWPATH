"use client";

import React, { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { api } from "@/lib/api";
import { ConceptSummary } from "@/types";

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: string[];
  is_ai?: boolean;
}

export default function TeachingCompanionPage() {
  const searchParams = useSearchParams();
  const initialConcept = searchParams.get("concept") || "variables_intro";

  const [concepts, setConcepts] = useState<ConceptSummary[]>([]);
  const [selectedConcept, setSelectedConcept] = useState<string>(initialConcept);
  const [inputQuestion, setInputQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hello! I am your AI Teaching Companion. I explain Python programming fundamentals strictly grounded in the verified Knowledge Genome curriculum. What concept would you like to explore?",
      is_ai: true,
      sources: ["Knowledge Genome Core Notes"],
    },
  ]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const loadConcepts = async () => {
      try {
        const list = await api.getGenomeConcepts();
        setConcepts(list);
      } catch (err) {
        console.error("Failed to load concepts:", err);
      }
    };
    loadConcepts();
  }, []);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputQuestion.trim() || loading) return;

    const userQ = inputQuestion.trim();
    setInputQuestion("");
    setMessages((prev) => [...prev, { role: "user", content: userQ }]);
    setLoading(true);

    try {
      const res = await api.askTeachingCompanion(selectedConcept, userQ);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: res.explanation,
          sources: res.sources,
          is_ai: res.is_ai,
        },
      ]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Apologies, I encountered an error: ${err?.message || "Safety or service timeout"}. Please try again.`,
          is_ai: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto flex flex-col h-[calc(100vh-140px)]">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4 flex-shrink-0">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xl">🤖</span>
            <h1 className="text-2xl font-extrabold text-white">AI Teaching Companion</h1>
          </div>
          <p className="mt-1 text-xs text-slate-400">
            Grounded educational tutor. Strictly validated for hallucination prevention and zero outcome promises.
          </p>
        </div>

        {/* Concept Focus Dropdown */}
        <div className="flex items-center space-x-2">
          <label className="text-xs text-slate-400">Focus Concept:</label>
          <select
            value={selectedConcept}
            onChange={(e) => setSelectedConcept(e.target.value)}
            className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-1.5 text-xs text-white focus:border-indigo-500 focus:outline-none"
          >
            {concepts.map((c) => (
              <option key={c.slug} value={c.slug}>
                {c.title} ({c.slug})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto space-y-4 p-4 rounded-2xl border border-slate-800 bg-slate-900/40">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`flex items-start gap-2.5 ${m.role === "user" ? "flex-row-reverse" : "flex-row"}`}
          >
            {m.role === "user" && (
              <div className="h-8 w-8 rounded-full bg-white p-0.5 border border-indigo-400/50 overflow-hidden flex-shrink-0 shadow-sm mt-1">
                <img
                  src="/images/knowpath-avatar.jpg"
                  alt="Learner"
                  className="h-full w-full rounded-full object-cover"
                />
              </div>
            )}
            {m.role === "assistant" && (
              <div className="h-8 w-8 rounded-xl bg-indigo-950 border border-indigo-600/50 flex items-center justify-center flex-shrink-0 text-base shadow-sm mt-1">
                🤖
              </div>
            )}

            <div
              className={`max-w-2xl rounded-2xl p-4 text-xs sm:text-sm leading-relaxed ${
                m.role === "user"
                  ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/20"
                  : "bg-slate-950 border border-slate-800 text-slate-200"
              }`}
            >
              {m.role === "assistant" && (
                <div className="flex items-center space-x-2 mb-2 pb-2 border-b border-slate-800/80">
                  <span className="rounded bg-indigo-950 border border-indigo-700/60 px-1.5 py-0.5 text-[10px] font-bold text-indigo-300">
                    [AI-Generated]
                  </span>
                  <span className="text-[10px] text-slate-400">Verified Teaching Tutor</span>
                </div>
              )}

              <p className="whitespace-pre-wrap">{m.content}</p>

              {m.sources && m.sources.length > 0 && (
                <div className="mt-3 pt-2 border-t border-slate-800 text-[11px] text-slate-400">
                  <span className="font-semibold text-slate-300">Sources: </span>
                  {m.sources.join(", ")}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex items-center space-x-2 text-xs text-slate-400 p-2">
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent"></div>
            <span>Grounding response in curriculum sources...</span>
          </div>
        )}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSend} className="flex items-center space-x-3 flex-shrink-0">
        <input
          type="text"
          value={inputQuestion}
          onChange={(e) => setInputQuestion(e.target.value)}
          placeholder={`Ask about ${selectedConcept.replace("_", " ")} (e.g. why is a default list argument shared?)...`}
          className="flex-1 rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-xs sm:text-sm text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
        />
        <button
          type="submit"
          disabled={loading || !inputQuestion.trim()}
          className="rounded-xl bg-indigo-600 px-5 sm:px-6 py-3 text-xs sm:text-sm font-semibold text-white shadow-lg shadow-indigo-600/20 hover:bg-indigo-500 disabled:opacity-50 transition-all cursor-pointer active:scale-95 select-none"
        >
          Send
        </button>
      </form>

      {/* Disclaimer */}
      <div className="text-center text-[10px] text-slate-500 flex-shrink-0">
        AI responses are grounded in verified Knowledge Genome texts. Scores are calculated deterministically by the
        backend engine, never by LLMs.
      </div>
    </div>
  );
}
