import React from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Link from "next/link";

export default function FeaturesPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Navbar />

      <main className="flex-1 py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">Capabilities</span>
            <h1 className="mt-2 text-4xl sm:text-5xl font-extrabold text-white">Platform Features</h1>
            <p className="mt-4 text-base sm:text-lg text-slate-400">
              Every feature of KNOWPATH operates as part of a coherent, verifiable intelligence loop.
            </p>
          </div>

          <div className="space-y-16">
            {/* Feature 1 */}
            <div id="cognitive-twin" className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center rounded-3xl border border-slate-800 bg-slate-900/40 p-8 sm:p-12">
              <div>
                <span className="rounded bg-indigo-950 border border-indigo-700/60 px-2.5 py-1 text-xs font-semibold text-indigo-300">
                  Feature 01
                </span>
                <h2 className="mt-3 text-2xl sm:text-3xl font-bold text-white">Cognitive Twin</h2>
                <p className="mt-4 text-slate-300 text-sm leading-relaxed">
                  Your digital knowledge representation. Rather than an arbitrary single percentage, each concept is
                  modeled as a probability density function. You can inspect exact 80% credible interval bounds,
                  underlying evidence items, recency decay penalties, and snapshot trends over time.
                </p>
                <div className="mt-6 flex flex-wrap gap-2 text-xs">
                  <span className="px-2.5 py-1 rounded-md bg-slate-800 text-slate-300">Beta(α, β) Bayesian Model</span>
                  <span className="px-2.5 py-1 rounded-md bg-slate-800 text-slate-300">60-Day Recency Half-Life</span>
                  <span className="px-2.5 py-1 rounded-md bg-slate-800 text-slate-300">Dispute Halving</span>
                </div>
              </div>
              <div className="rounded-2xl border border-slate-800 bg-slate-950 p-6 font-mono text-xs text-slate-300">
                <div className="text-slate-500 pb-2 border-b border-slate-800"># Cognitive Twin API Sample</div>
                <pre className="mt-3 text-indigo-300 overflow-x-auto">
{`{
  "concept": "list_mutability",
  "mastery_score": 0.84,
  "confidence": 0.91,
  "credible_interval": [0.76, 0.92],
  "evidence_count": 6,
  "primary_source": "assessment_verified",
  "why_this_score": "3 correct code_reading items, 1 correct predict_bug; 0 active disputes"
}`}
                </pre>
              </div>
            </div>

            {/* Feature 2 */}
            <div id="knowledge-genome" className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center rounded-3xl border border-slate-800 bg-slate-900/40 p-8 sm:p-12">
              <div>
                <span className="rounded bg-teal-950 border border-teal-700/60 px-2.5 py-1 text-xs font-semibold text-teal-300">
                  Feature 02
                </span>
                <h2 className="mt-3 text-2xl sm:text-3xl font-bold text-white">Knowledge Genome DAG</h2>
                <p className="mt-4 text-slate-300 text-sm leading-relaxed">
                  A foundational curriculum graph of 79 core Python concepts connected through 118 prerequisite edges.
                  Navigate concepts by category (types, control flow, functions, OOP, data structures, exceptions) and
                  inspect prerequisite chains before attempting new material.
                </p>
                <div className="mt-6 flex flex-wrap gap-2 text-xs">
                  <span className="px-2.5 py-1 rounded-md bg-slate-800 text-slate-300">Cycle-Free DAG</span>
                  <span className="px-2.5 py-1 rounded-md bg-slate-800 text-slate-300">Foundation Bonus</span>
                  <span className="px-2.5 py-1 rounded-md bg-slate-800 text-slate-300">79 Verified Modules</span>
                </div>
              </div>
              <div className="rounded-2xl border border-slate-800 bg-slate-950 p-6 font-mono text-xs text-slate-300">
                <div className="text-slate-500 pb-2 border-b border-slate-800"># DAG Prerequisite Chain</div>
                <div className="mt-3 space-y-2 text-teal-300">
                  <div>variables_intro</div>
                  <div className="pl-4">↳ data_types_basics</div>
                  <div className="pl-8">↳ list_basics</div>
                  <div className="pl-12">↳ list_mutability (Foundation)</div>
                  <div className="pl-16 text-indigo-400">↳ shallow_vs_deep_copy</div>
                </div>
              </div>
            </div>

            {/* Feature 3 */}
            <div id="adaptive-learning" className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center rounded-3xl border border-slate-800 bg-slate-900/40 p-8 sm:p-12">
              <div>
                <span className="rounded bg-sky-950 border border-sky-700/60 px-2.5 py-1 text-xs font-semibold text-sky-300">
                  Feature 03
                </span>
                <h2 className="mt-3 text-2xl sm:text-3xl font-bold text-white">Adaptive Diagnostic & Quizzes</h2>
                <p className="mt-4 text-slate-300 text-sm leading-relaxed">
                  Our assessment algorithm prioritizes questions that maximize information gain on your knowledge
                  frontier. Each distractor choice maps to a curated misconception trap, diagnosing subtle conceptual
                  flaws (e.g. integer division vs floor division, mutable default arguments).
                </p>
              </div>
              <div className="rounded-2xl border border-slate-800 bg-slate-950 p-6 text-xs text-slate-300">
                <div className="text-slate-500 pb-2 border-b border-slate-800 font-mono"># Adaptive Question Engine</div>
                <div className="mt-3 p-3 rounded-lg bg-slate-900 border border-slate-800">
                  <p className="font-semibold text-white">def append_to(item, target=[]):</p>
                  <p className="pl-4 font-mono text-slate-400">target.append(item)</p>
                  <p className="pl-4 font-mono text-slate-400">return target</p>
                  <p className="mt-2 text-amber-300">⚠️ Distractor: &quot;New list created on each call&quot;</p>
                  <p className="text-[11px] text-slate-400">Detected: MISCON_DEFAULT_ARG_EVAL</p>
                </div>
              </div>
            </div>

            {/* Feature 4 */}
            <div id="futurepath" className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center rounded-3xl border border-slate-800 bg-slate-900/40 p-8 sm:p-12">
              <div>
                <span className="rounded bg-purple-950 border border-purple-700/60 px-2.5 py-1 text-xs font-semibold text-purple-300">
                  Feature 04
                </span>
                <h2 className="mt-3 text-2xl sm:text-3xl font-bold text-white">FuturePath Simulator</h2>
                <p className="mt-4 text-slate-300 text-sm leading-relaxed">
                  Explore career and capability tracks—from Backend Engineering to Data Analytics—and simulate your
                  readiness based strictly on verified concept mastery. Never promises jobs; shows unmastered
                  prerequisite bottlenecks.
                </p>
              </div>
              <div className="rounded-2xl border border-slate-800 bg-slate-950 p-6 text-xs text-slate-300">
                <div className="text-slate-500 pb-2 border-b border-slate-800 font-mono"># Capability Readiness</div>
                <div className="mt-3 space-y-3">
                  <div>
                    <div className="flex justify-between text-xs font-medium mb-1">
                      <span>Python for Backend APIs</span>
                      <span className="text-indigo-400">68% Ready</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-2">
                      <div className="bg-indigo-500 h-2 rounded-full" style={{ width: "68%" }}></div>
                    </div>
                  </div>
                  <p className="text-[11px] text-slate-400">
                    Missing Foundations: <span className="text-rose-400">exception_handling, async_basics</span>
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-16 text-center">
            <Link
              href="/register"
              className="w-full sm:w-auto inline-block rounded-xl bg-indigo-600 px-8 py-3.5 text-base font-semibold text-white shadow-lg shadow-indigo-600/30 hover:bg-indigo-500 transition-all cursor-pointer active:scale-95 select-none"
            >
              Start Your Free Assessment
            </Link>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
