"use client";

import React, { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { TwinPageData } from "@/types";
import { useAuthStore } from "@/stores/auth";

export default function PortfolioPage() {
  const { user } = useAuthStore();
  const [twin, setTwin] = useState<TwinPageData | null>(null);
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState(false);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const data = await api.getTwin();
        setTwin(data);
      } catch (err) {
        console.error("Failed to load portfolio twin data:", err);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const handleExport = async () => {
    try {
      setExporting(true);
      const blob = await api.exportData();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `knowpath_capability_proof_${new Date().toISOString().split("T")[0]}.json`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err: any) {
      alert(`Export failed: ${err?.message || "Unknown error"}`);
    } finally {
      setExporting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="flex items-center space-x-3 text-slate-400">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent"></div>
          <span className="text-sm">Synthesizing verifiable capability proof...</span>
        </div>
      </div>
    );
  }

  const verifiedItems = twin?.mastery_list?.filter((m) => m.source_type === "assessment_verified") || [];
  const aiItems = twin?.mastery_list?.filter((m) => m.source_type === "ai_estimated") || [];
  const selfItems = twin?.mastery_list?.filter((m) => m.source_type === "self_reported") || [];

  return (
    <div className="space-y-8 max-w-5xl">
      {/* Header with Learner Identity Card */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 border-b border-slate-800 pb-6">
        <div className="flex items-start space-x-4">
          <div className="relative h-14 w-14 rounded-2xl bg-white p-1 border border-indigo-400/50 shadow-lg shadow-indigo-600/20 overflow-hidden flex-shrink-0">
            <img
              src="/images/knowpath-avatar.jpg"
              alt="Learner Profile"
              className="h-full w-full rounded-xl object-cover"
            />
          </div>
          <div>
            <div className="inline-flex items-center space-x-2 rounded-full bg-indigo-950/80 border border-indigo-700/50 px-3 py-0.5 text-xs font-semibold text-indigo-300 mb-1.5">
              <span>Verified Learner Portfolio</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
              {user?.email ? `${user.email}'s Portfolio` : "Capability Portfolio"}
            </h1>
            <p className="mt-1 text-xs sm:text-sm text-slate-400">
              A cryptographically signed, audit-ready representation of what you demonstrably know.
            </p>
          </div>
        </div>

        <div className="w-full sm:w-auto">
          <button
            onClick={handleExport}
            disabled={exporting}
            className="w-full sm:w-auto rounded-xl bg-indigo-600 px-5 py-3 text-xs font-semibold text-white hover:bg-indigo-500 disabled:opacity-50 transition-all cursor-pointer active:scale-95 select-none flex items-center justify-center space-x-2 shadow-lg shadow-indigo-600/20"
          >
            <span>📥</span>
            <span>{exporting ? "Generating Archive..." : "Export Capability Proof (JSON)"}</span>
          </button>
        </div>
      </div>

      {/* Evidence Hierarchy Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="rounded-2xl border border-indigo-900/60 bg-indigo-950/20 p-6">
          <div className="text-xs font-bold uppercase tracking-wider text-indigo-400">Assessment-Verified</div>
          <div className="mt-2 text-3xl font-bold text-white">{verifiedItems.length}</div>
          <p className="mt-1 text-xs text-slate-400">Weight: 1.00 (Empirically graded items)</p>
        </div>

        <div className="rounded-2xl border border-amber-900/60 bg-amber-950/20 p-6">
          <div className="text-xs font-bold uppercase tracking-wider text-amber-400">AI-Estimated</div>
          <div className="mt-2 text-3xl font-bold text-white">{aiItems.length}</div>
          <p className="mt-1 text-xs text-slate-400">Weight: 0.30 (Tutor & companion interaction)</p>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400">Self-Reported</div>
          <div className="mt-2 text-3xl font-bold text-white">{selfItems.length}</div>
          <p className="mt-1 text-xs text-slate-400">Weight: 0.10 (Initial onboarding rating)</p>
        </div>
      </div>

      {/* Verified Skills List */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 sm:p-8">
        <h2 className="text-lg font-bold text-white mb-4">Empirically Verified Capabilities</h2>
        <div className="space-y-3">
          {verifiedItems.length > 0 ? (
            verifiedItems.map((item) => (
              <div
                key={item.concept_id}
                className="p-4 rounded-xl border border-slate-800 bg-slate-950 flex items-center justify-between"
              >
                <div>
                  <h3 className="text-sm font-bold text-white">{item.concept_title || item.concept_id}</h3>
                  <div className="text-xs text-slate-500 font-mono mt-0.5">
                    Confidence: {(item.confidence * 100).toFixed(0)}% | Credible Interval: [
                    {(item.credible_interval_low * 100).toFixed(0)}% - {(item.credible_interval_high * 100).toFixed(0)}%]
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-base font-bold text-emerald-400">
                    {(item.mastery_score * 100).toFixed(0)}%
                  </span>
                  <span className="block text-[10px] text-slate-500">Posterior Mean</span>
                </div>
              </div>
            ))
          ) : (
            <p className="text-sm text-slate-400 py-4 text-center">
              No assessment-verified items yet. Complete the Adaptive Diagnostic to establish verified capabilities.
            </p>
          )}
        </div>
      </div>

      {/* Integrity & Compliance Disclaimer */}
      <div className="p-4 rounded-xl border border-slate-800 bg-slate-950 text-xs text-slate-400 leading-relaxed">
        <strong>Charter Notice:</strong> KnowPath issues evidence records, not outcome guarantees. Demonstrable mastery
        reflects responses to diagnostic and retrieval items evaluated under deterministic scoring equations.
      </div>
    </div>
  );
}
