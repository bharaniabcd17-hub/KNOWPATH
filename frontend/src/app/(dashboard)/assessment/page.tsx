"use client";

import React from "react";
import Link from "next/link";

export default function AssessmentHubPage() {
  return (
    <div className="space-y-8 max-w-5xl">
      {/* Header */}
      <div className="border-b border-slate-800 pb-6">
        <div className="inline-flex items-center space-x-2 rounded-full bg-indigo-950/80 border border-indigo-700/50 px-3 py-0.5 text-xs font-semibold text-indigo-300 mb-2">
          <span>Item Selection via Information Gain</span>
        </div>
        <h1 className="text-3xl font-extrabold text-white">Assessment & Diagnostic Engine</h1>
        <p className="mt-1 text-sm text-slate-400">
          Calibrate your Cognitive Twin using verifiable assessment items. Every distractor is tagged with diagnostic
          misconception traps.
        </p>
      </div>

      {/* Featured Diagnostic Hero Card */}
      <div className="rounded-2xl border border-indigo-500/40 bg-gradient-to-r from-indigo-950/40 via-slate-900 to-slate-900 p-8 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-3">
            <span className="rounded bg-indigo-900/60 border border-indigo-700/80 px-2.5 py-1 text-xs font-bold text-indigo-200">
              RECOMMENDED STARTING POINT
            </span>
            <h2 className="text-2xl font-bold text-white">Full Adaptive Diagnostic</h2>
            <p className="text-sm text-slate-300 max-w-xl leading-relaxed">
              15-20 items served adaptively. The engine starts at the core foundations of Python and navigates the
              prerequisite DAG to pinpoint your exact knowledge boundary.
            </p>
            <div className="flex flex-wrap gap-4 text-xs text-slate-400 pt-2">
              <span>⏱️ ~15-20 Minutes</span>
              <span>🎯 Dynamic Frontier Selection</span>
              <span>⚖️ Full Beta-Weight Calibration</span>
            </div>
          </div>

          <div className="w-full md:w-auto">
            <Link
              href="/assessment/diagnostic"
              className="w-full md:w-auto inline-block rounded-xl bg-indigo-600 px-6 py-3.5 text-sm font-bold text-white shadow-lg shadow-indigo-600/30 hover:bg-indigo-500 transition-all text-center cursor-pointer active:scale-95 select-none"
            >
              Start Diagnostic Session →
            </Link>
          </div>
        </div>
      </div>

      {/* Assessment Question Types Explanation */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6 sm:p-8">
        <h3 className="text-lg font-bold text-white mb-4">Supported Question Paradigms</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
            <div className="text-2xl mb-2">💻</div>
            <h4 className="text-sm font-bold text-white">Code Reading (&quot;What does this output?&quot;)</h4>
            <p className="mt-1 text-xs text-slate-400 leading-relaxed">
              Traces pointer aliasing, mutability, scope resolution, and return values without executing random code in
              sandboxes.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
            <div className="text-2xl mb-2">🐛</div>
            <h4 className="text-sm font-bold text-white">Predict-the-Bug</h4>
            <p className="mt-1 text-xs text-slate-400 leading-relaxed">
              Identifies syntax bugs, runtime TypeError/IndexError traps, and logic flaws in idiomatic Python.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
            <div className="text-2xl mb-2">🎛️</div>
            <h4 className="text-sm font-bold text-white">Multi-Select & Concept MCQ</h4>
            <p className="mt-1 text-xs text-slate-400 leading-relaxed">
              Evaluates deep conceptual nuances. Distractors represent 34 known mental misconception traps.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
