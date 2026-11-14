"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { MasteryItem, TwinPageData } from "@/types";

export default function CognitiveTwinPage() {
  const [twin, setTwin] = useState<TwinPageData | null>(null);
  const [snapshots, setSnapshots] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedConcept, setSelectedConcept] = useState<MasteryItem | null>(null);
  const [search, setSearch] = useState("");
  const [filterTier, setFilterTier] = useState<"all" | "mastered" | "frontier" | "uncalibrated">("all");

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const [twinRes, snapRes] = await Promise.allSettled([
          api.getTwin(),
          api.getTwinSnapshots(),
        ]);
        if (twinRes.status === "fulfilled") {
          setTwin(twinRes.value);
          if (twinRes.value.mastery_list?.length > 0) {
            setSelectedConcept(twinRes.value.mastery_list[0]);
          }
        }
        if (snapRes.status === "fulfilled") {
          setSnapshots(snapRes.value);
        }
      } catch (err) {
        console.error("Twin loading error:", err);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="flex items-center space-x-3 text-slate-400">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent"></div>
          <span className="text-sm">Retrieving Cognitive Twin probabilistic model...</span>
        </div>
      </div>
    );
  }

  const masteryList = twin?.mastery_list || [];

  const filtered = masteryList.filter((item) => {
    const matchesSearch =
      item.concept_id.toLowerCase().includes(search.toLowerCase()) ||
      (item.concept_title && item.concept_title.toLowerCase().includes(search.toLowerCase()));

    if (!matchesSearch) return false;

    if (filterTier === "mastered") return item.mastery_score >= 0.7;
    if (filterTier === "frontier") return item.mastery_score >= 0.3 && item.mastery_score < 0.7;
    if (filterTier === "uncalibrated") return item.mastery_score < 0.3;
    return true;
  });

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="inline-flex items-center space-x-2 rounded-full bg-indigo-950/80 border border-indigo-700/50 px-3 py-0.5 text-xs font-semibold text-indigo-300 mb-2">
            <span>Probabilistic Digital Twin</span>
          </div>
          <h1 className="text-3xl font-extrabold text-white">Your Cognitive Twin</h1>
          <p className="mt-1 text-sm text-slate-400">
            A dynamic Bayesian model of your knowledge state across 79 Python concepts, calibrated by empirical evidence.
          </p>
        </div>

        <div className="w-full sm:w-auto">
          <Link
            href="/assessment/diagnostic"
            className="w-full sm:w-auto inline-block text-center rounded-xl bg-indigo-600 px-5 py-2.5 text-xs sm:text-sm font-semibold text-white shadow-lg shadow-indigo-600/20 hover:bg-indigo-500 transition-all cursor-pointer active:scale-95 select-none"
          >
            Calibrate via Diagnostic
          </Link>
        </div>
      </div>

      {/* Snapshot History Strip (if any) */}
      {snapshots.length > 0 && (
        <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-4">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2 block">
            Twin Evolution History ({snapshots.length} snapshots recorded)
          </span>
          <div className="flex items-center space-x-4 overflow-x-auto py-1 text-xs">
            {snapshots.map((snap, i) => (
              <div
                key={snap.id || i}
                className="flex-shrink-0 px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-slate-300"
              >
                <div className="text-[10px] text-slate-500">
                  {new Date(snap.created_at).toLocaleDateString()}
                </div>
                <div className="font-bold text-indigo-300 mt-0.5">
                  Avg: {((snap.mean_mastery || 0) * 100).toFixed(0)}%
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Filter and Search Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="w-full sm:w-80">
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search concept (e.g. loops, mutability)..."
            className="w-full rounded-lg border border-slate-700 bg-slate-900 px-3.5 py-2 text-xs text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
          />
        </div>

        <div className="flex flex-wrap gap-2 w-full sm:w-auto">
          <button
            onClick={() => setFilterTier("all")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all cursor-pointer active:scale-95 select-none ${
              filterTier === "all" ? "bg-indigo-600 text-white shadow-sm" : "bg-slate-900 text-slate-400 hover:text-white hover:bg-slate-800"
            }`}
          >
            All ({masteryList.length})
          </button>
          <button
            onClick={() => setFilterTier("mastered")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all cursor-pointer active:scale-95 select-none ${
              filterTier === "mastered" ? "bg-emerald-600 text-white shadow-sm" : "bg-slate-900 text-slate-400 hover:text-white hover:bg-slate-800"
            }`}
          >
            Mastered (&ge;70%)
          </button>
          <button
            onClick={() => setFilterTier("frontier")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all cursor-pointer active:scale-95 select-none ${
              filterTier === "frontier" ? "bg-amber-600 text-white shadow-sm" : "bg-slate-900 text-slate-400 hover:text-white hover:bg-slate-800"
            }`}
          >
            Learning Frontier (30-69%)
          </button>
          <button
            onClick={() => setFilterTier("uncalibrated")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all cursor-pointer active:scale-95 select-none ${
              filterTier === "uncalibrated" ? "bg-slate-700 text-white shadow-sm" : "bg-slate-900 text-slate-400 hover:text-white hover:bg-slate-800"
            }`}
          >
            Uncalibrated (&lt;30%)
          </button>
        </div>
      </div>

      {/* Split View: Concept Mastery Table + "Why This Score" Detail Drawer */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Concepts Table */}
        <div className="lg:col-span-2 rounded-2xl border border-slate-800 bg-slate-900/60 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950 text-slate-400 uppercase font-semibold border-b border-slate-800">
                <tr>
                  <th className="px-4 py-3">Concept</th>
                  <th className="px-4 py-3">Mastery</th>
                  <th className="px-4 py-3">80% Credible Interval</th>
                  <th className="px-4 py-3">Confidence</th>
                  <th className="px-4 py-3">Source Type</th>
                  <th className="px-4 py-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-200">
                {filtered.map((item) => {
                  const isSelected = selectedConcept?.concept_id === item.concept_id;
                  const pct = (item.mastery_score * 100).toFixed(0);

                  return (
                    <tr
                      key={item.concept_id}
                      onClick={() => setSelectedConcept(item)}
                      className={`cursor-pointer hover:bg-slate-800/50 transition-colors ${
                        isSelected ? "bg-indigo-950/40 border-l-2 border-indigo-500" : ""
                      }`}
                    >
                      <td className="px-4 py-3.5 font-medium text-white">
                        <div>{item.concept_title || item.concept_id}</div>
                        <div className="text-[10px] text-slate-500 font-mono">{item.concept_id}</div>
                      </td>
                      <td className="px-4 py-3.5">
                        <div className="flex items-center space-x-2">
                          <span
                            className={`font-bold ${
                              item.mastery_score >= 0.7
                                ? "text-emerald-400"
                                : item.mastery_score >= 0.3
                                ? "text-amber-400"
                                : "text-slate-400"
                            }`}
                          >
                            {pct}%
                          </span>
                        </div>
                      </td>
                      <td className="px-4 py-3.5 text-slate-400 font-mono">
                        [{(item.credible_interval_low * 100).toFixed(0)}% -{" "}
                        {(item.credible_interval_high * 100).toFixed(0)}%]
                      </td>
                      <td className="px-4 py-3.5">
                        <span className="text-slate-300">{(item.confidence * 100).toFixed(0)}%</span>
                      </td>
                      <td className="px-4 py-3.5 capitalize text-slate-400">
                        <span
                          className={`inline-block px-2 py-0.5 rounded text-[10px] font-semibold ${
                            item.source_type === "assessment_verified"
                              ? "bg-indigo-950 text-indigo-300 border border-indigo-800/60"
                              : item.source_type === "ai_estimated"
                              ? "bg-amber-950 text-amber-300 border border-amber-800/60"
                              : "bg-slate-800 text-slate-400"
                          }`}
                        >
                          {item.source_type.replace("_", " ")}
                        </span>
                      </td>
                      <td className="px-4 py-3.5 text-right">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            setSelectedConcept(item);
                          }}
                          className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold"
                        >
                          Inspect →
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Explainability Drawer: "Why This Score" */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 space-y-6">
          <div className="flex items-center justify-between pb-4 border-b border-slate-800">
            <h2 className="text-base font-bold text-white flex items-center space-x-2">
              <span>🔍</span>
              <span>Why This Score?</span>
            </h2>
            <span className="text-[10px] text-indigo-400 uppercase font-semibold">Explainability Layer</span>
          </div>

          {selectedConcept ? (
            <div className="space-y-5 text-xs text-slate-300">
              <div>
                <span className="text-slate-500 uppercase text-[10px] font-semibold tracking-wider block">
                  Concept Identifier
                </span>
                <h3 className="text-lg font-bold text-white mt-0.5">
                  {selectedConcept.concept_title || selectedConcept.concept_id}
                </h3>
                <span className="text-[11px] font-mono text-indigo-400">{selectedConcept.concept_id}</span>
              </div>

              {/* Score breakdown metrics */}
              <div className="grid grid-cols-2 gap-3 p-3.5 rounded-xl bg-slate-950 border border-slate-800">
                <div>
                  <div className="text-slate-500 text-[10px]">Mastery (Mean)</div>
                  <div className="text-xl font-bold text-white">
                    {(selectedConcept.mastery_score * 100).toFixed(1)}%
                  </div>
                </div>
                <div>
                  <div className="text-slate-500 text-[10px]">Confidence</div>
                  <div className="text-xl font-bold text-indigo-400">
                    {(selectedConcept.confidence * 100).toFixed(1)}%
                  </div>
                </div>
                <div>
                  <div className="text-slate-500 text-[10px]">Alpha parameter</div>
                  <div className="font-mono text-slate-200">{selectedConcept.alpha.toFixed(2)}</div>
                </div>
                <div>
                  <div className="text-slate-500 text-[10px]">Beta parameter</div>
                  <div className="font-mono text-slate-200">{selectedConcept.beta.toFixed(2)}</div>
                </div>
              </div>

              {/* Verbal Explanation */}
              <div>
                <span className="text-slate-500 uppercase text-[10px] font-semibold tracking-wider block mb-1">
                  Deterministic Audit Explanation
                </span>
                <p className="leading-relaxed bg-slate-950 p-3 rounded-lg border border-slate-800 text-slate-300">
                  {selectedConcept.why_this_score ||
                    `Calculated using Beta distribution with alpha=${selectedConcept.alpha.toFixed(
                      1
                    )} and beta=${selectedConcept.beta.toFixed(
                      1
                    )}. Score incorporates source hierarchy weights, 60-day recency half-life, and dispute factor.`}
                </p>
              </div>

              {/* Actions */}
              <div className="pt-2 flex flex-col space-y-2">
                <Link
                  href={`/genome/${selectedConcept.concept_id}`}
                  className="w-full text-center rounded-lg bg-indigo-600 py-2.5 font-semibold text-white hover:bg-indigo-500 transition-all cursor-pointer active:scale-95 select-none block"
                >
                  View Concept Curriculum Notes
                </Link>

                <Link
                  href={`/disputes?target_id=${selectedConcept.concept_id}&target_type=score`}
                  className="w-full text-center rounded-lg border border-slate-800 bg-slate-950 py-2.5 font-medium text-slate-300 hover:text-white hover:bg-slate-900 transition-all cursor-pointer active:scale-95 select-none block"
                >
                  ⚖️ Challenge / Dispute This Score
                </Link>
              </div>
            </div>
          ) : (
            <div className="text-center py-8 text-slate-500">
              Select a concept from the table to inspect its evidence provenance.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
