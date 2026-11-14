"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { ConceptDetail } from "@/types";

interface ConceptDetailViewProps {
  slug: string;
}

export default function ConceptDetailView({ slug }: ConceptDetailViewProps) {
  const [concept, setConcept] = useState<ConceptDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) return;
    const fetchDetail = async () => {
      try {
        setLoading(true);
        const data = await api.getConceptDetail(slug);
        setConcept(data);
      } catch (err: any) {
        setError(err?.message || "Failed to load concept detail");
      } finally {
        setLoading(false);
      }
    };
    fetchDetail();
  }, [slug]);

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="flex items-center space-x-3 text-slate-400">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-teal-500 border-t-transparent"></div>
          <span className="text-sm">Loading curriculum notes for {slug}...</span>
        </div>
      </div>
    );
  }

  if (error || !concept) {
    return (
      <div className="rounded-2xl border border-rose-900/50 bg-rose-950/20 p-8 text-center">
        <h2 className="text-xl font-bold text-white">Concept Not Found</h2>
        <p className="mt-2 text-sm text-rose-300">
          {error || "The requested concept slug does not exist in the Genome."}
        </p>
        <Link
          href="/genome"
          className="mt-4 inline-block rounded-xl bg-slate-800 px-4 py-2 text-xs font-semibold text-white hover:bg-slate-700 transition-colors"
        >
          ← Return to Knowledge Genome
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-5xl">
      {/* Back button & Breadcrumb */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <Link
          href="/genome"
          className="inline-flex items-center space-x-1.5 text-xs text-slate-400 hover:text-white transition-colors cursor-pointer"
        >
          <span>←</span>
          <span>Back to Knowledge Genome</span>
        </Link>

        <div className="flex items-center space-x-2">
          <Link
            href={`/companion?concept=${concept.slug}`}
            className="w-full sm:w-auto text-center rounded-xl bg-indigo-600 px-4 py-2 text-xs font-semibold text-white hover:bg-indigo-500 transition-all cursor-pointer active:scale-95 shadow-lg shadow-indigo-600/20"
          >
            Ask AI Companion About This Concept
          </Link>
        </div>
      </div>

      {/* Main Header Card */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 sm:p-8">
        <div className="flex flex-wrap items-center gap-2 mb-3">
          <span
            className={`px-2.5 py-0.5 rounded text-[11px] font-semibold uppercase ${
              String(concept.difficulty) === "beginner"
                ? "bg-emerald-950 text-emerald-300 border border-emerald-800/50"
                : String(concept.difficulty) === "intermediate"
                ? "bg-amber-950 text-amber-300 border border-amber-800/50"
                : "bg-purple-950 text-purple-300 border border-purple-800/50"
            }`}
          >
            {concept.difficulty}
          </span>
          <span className="text-xs text-slate-500 font-mono">#{concept.slug}</span>
        </div>

        <h1 className="text-2xl sm:text-4xl font-extrabold text-white">{concept.title}</h1>
        <p className="mt-3 text-sm sm:text-base text-slate-300 leading-relaxed">{concept.description}</p>
      </div>

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Notes & Examples */}
        <div className="lg:col-span-2 space-y-6">
          <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6 sm:p-8">
            <h2 className="text-lg font-bold text-white mb-4 pb-2 border-b border-slate-800">
              Curriculum Notes & Examples
            </h2>
            <div className="prose prose-invert max-w-none text-slate-300 text-sm leading-relaxed whitespace-pre-wrap font-sans">
              {concept.content || "No extended study notes currently stored for this concept."}
            </div>
          </div>

          {/* Linked Questions Bank */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
            <h3 className="text-base font-bold text-white mb-2">Assessment Calibration Bank</h3>
            <p className="text-xs text-slate-400">
              This concept is calibrated using{" "}
              <strong className="text-white">{concept.questions_count || 5}+</strong> verified questions
              across multiple choice, code reading, and predict-the-bug formats.
            </p>
            <div className="mt-4">
              <Link
                href="/assessment/diagnostic"
                className="w-full sm:w-auto inline-block text-center rounded-xl bg-teal-600 px-5 py-2.5 text-xs font-semibold text-white hover:bg-teal-500 transition-all cursor-pointer active:scale-95 shadow-md shadow-teal-600/20"
              >
                Test Knowledge on This Concept
              </Link>
            </div>
          </div>
        </div>

        {/* Right Column: Graph Connections */}
        <div className="space-y-6">
          {/* Prerequisites */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-3 flex items-center space-x-2">
              <span>⬅️</span>
              <span>Prerequisites ({concept.prerequisites?.length || 0})</span>
            </h3>

            {concept.prerequisites && concept.prerequisites.length > 0 ? (
              <div className="space-y-2">
                {concept.prerequisites.map((p) => (
                  <Link
                    key={p}
                    href={`/genome/${p}`}
                    className="block p-2.5 rounded-lg border border-slate-800 bg-slate-950 hover:border-indigo-500 text-xs font-medium text-slate-200 transition-colors"
                  >
                    <span className="text-indigo-400 font-mono">↳</span> {p}
                  </Link>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-500">Root foundation concept. No prerequisites required.</p>
            )}
          </div>

          {/* Dependents */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-3 flex items-center space-x-2">
              <span>➡️</span>
              <span>Downstream Dependents ({concept.dependents?.length || 0})</span>
            </h3>

            {concept.dependents && concept.dependents.length > 0 ? (
              <div className="space-y-2">
                {concept.dependents.map((d) => (
                  <Link
                    key={d}
                    href={`/genome/${d}`}
                    className="block p-2.5 rounded-lg border border-slate-800 bg-slate-950 hover:border-teal-500 text-xs font-medium text-slate-200 transition-colors"
                  >
                    <span className="text-teal-400 font-mono">↳</span> {d}
                  </Link>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-500">Terminal leaf node in this curriculum partition.</p>
            )}
          </div>

          {/* Foundation Multiplier Indicator */}
          {concept.dependents && concept.dependents.length >= 2 && (
            <div className="rounded-xl border border-amber-900/60 bg-amber-950/20 p-4 text-xs text-amber-300">
              <span className="font-bold block mb-1">🌟 High-Leverage Foundation Node</span>
              This concept unblocks {concept.dependents.length} downstream topics. Mastering it provides a
              1.25x foundation bonus in roadmap generation.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
