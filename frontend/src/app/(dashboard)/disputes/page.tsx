"use client";

import React, { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { api } from "@/lib/api";
import { Dispute } from "@/types";

export default function DisputesPage() {
  const searchParams = useSearchParams();
  const initialTargetId = searchParams.get("target_id") || "";
  const initialTargetType = (searchParams.get("target_type") as "question" | "score") || "score";

  const [disputes, setDisputes] = useState<Dispute[]>([]);
  const [targetType, setTargetType] = useState<"question" | "score">(initialTargetType);
  const [targetId, setTargetId] = useState(initialTargetId);
  const [reason, setReason] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [loading, setLoading] = useState(true);
  const [statusMsg, setStatusMsg] = useState<string | null>(null);

  const fetchDisputes = async () => {
    try {
      setLoading(true);
      const list = await api.getMyDisputes();
      setDisputes(list);
    } catch (err) {
      console.error("Disputes fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDisputes();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!targetId || !reason) return;

    try {
      setSubmitting(true);
      await api.createDispute({
        target_type: targetType,
        target_id: targetId,
        reason,
      });
      setStatusMsg("Dispute filed successfully! The target weight is halved (0.5x) pending admin audit.");
      setReason("");
      setTargetId("");
      fetchDisputes();
    } catch (err: any) {
      setStatusMsg(`Failed to file dispute: ${err?.message || "Unknown error"}`);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-8 max-w-4xl">
      {/* Header */}
      <div className="border-b border-slate-800 pb-6">
        <div className="inline-flex items-center space-x-2 rounded-full bg-indigo-950/80 border border-indigo-700/50 px-3 py-0.5 text-xs font-semibold text-indigo-300 mb-2">
          <span>Explainability & Integrity Charter</span>
        </div>
        <h1 className="text-3xl font-extrabold text-white">Disputes & Score Integrity</h1>
        <p className="mt-1 text-sm text-slate-400">
          Learners have the sovereign right to challenge incorrect questions, ambiguous distractors, or flawed score
          updates.
        </p>
      </div>

      {/* Charter explanation */}
      <div className="p-4 rounded-xl border border-indigo-900/60 bg-indigo-950/20 text-xs text-indigo-200 leading-relaxed">
        <strong>Deterministic Dispute Policy:</strong> When a dispute is filed against a score or question, the scoring
        engine immediately applies a <span className="font-bold text-white">0.5x dispute factor</span> to that
        evidence weight in your Beta update, mitigating potential grading penalties until an administrator reviews the
        case.
      </div>

      {/* New Dispute Form */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 sm:p-8">
        <h2 className="text-lg font-bold text-white mb-4">File a Formal Dispute</h2>

        {statusMsg && (
          <div className="mb-4 p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-200">
            {statusMsg}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
                Target Type
              </label>
              <select
                value={targetType}
                onChange={(e) => setTargetType(e.target.value as "question" | "score")}
                className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3.5 py-2.5 text-sm text-white focus:border-indigo-500 focus:outline-none"
              >
                <option value="score">Concept Score</option>
                <option value="question">Question / Distractor</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
                Target Identifier (Concept Slug or Question ID)
              </label>
              <input
                type="text"
                required
                value={targetId}
                onChange={(e) => setTargetId(e.target.value)}
                placeholder="e.g. list_mutability"
                className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3.5 py-2.5 text-sm text-white focus:border-indigo-500 focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
              Reason for Dispute
            </label>
            <textarea
              required
              rows={3}
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              placeholder="Explain why the question wording was ambiguous or why the score evidence is contested..."
              className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3.5 py-2.5 text-sm text-white focus:border-indigo-500 focus:outline-none"
            ></textarea>
          </div>

          <button
            type="submit"
            disabled={submitting}
            className="w-full sm:w-auto rounded-xl bg-indigo-600 px-6 py-3 text-xs font-semibold text-white hover:bg-indigo-500 disabled:opacity-50 transition-all cursor-pointer active:scale-95 select-none shadow-lg shadow-indigo-600/20"
          >
            {submitting ? "Submitting Dispute..." : "Submit Formal Dispute"}
          </button>
        </form>
      </div>

      {/* Dispute History List */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 sm:p-8">
        <h2 className="text-lg font-bold text-white mb-4">Your Dispute Records</h2>

        {loading ? (
          <div className="py-4 text-xs text-slate-400">Loading disputes...</div>
        ) : disputes.length > 0 ? (
          <div className="space-y-3">
            {disputes.map((d) => (
              <div
                key={d.id}
                className="p-4 rounded-xl border border-slate-800 bg-slate-950 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs"
              >
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="font-mono text-indigo-400 font-bold">{d.target_id}</span>
                    <span className="capitalize text-slate-500">({d.target_type})</span>
                  </div>
                  <p className="mt-1 text-slate-300">{d.reason}</p>
                  {d.resolution_notes && (
                    <p className="mt-1 text-emerald-400 font-medium">Admin resolution: {d.resolution_notes}</p>
                  )}
                </div>

                <div className="flex sm:flex-col items-center sm:items-end justify-between sm:justify-center">
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-semibold uppercase ${
                      d.status === "open"
                        ? "bg-amber-950 text-amber-300 border border-amber-800/60"
                        : d.status === "resolved"
                        ? "bg-emerald-950 text-emerald-300 border border-emerald-800/60"
                        : "bg-slate-800 text-slate-400"
                    }`}
                  >
                    {d.status}
                  </span>
                  <span className="text-[10px] text-slate-500 mt-1">
                    {d.created_at ? new Date(d.created_at).toLocaleDateString() : "Recently"}
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-500 py-4 text-center">No active or historical disputes recorded.</p>
        )}
      </div>
    </div>
  );
}
