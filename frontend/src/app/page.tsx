"use client";

import React, { useState } from "react";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default function HomePage() {
  const [activeTab, setActiveTab] = useState<"twin" | "genome" | "scoring">("twin");

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Navbar />

      <main className="flex-1">
        {/* PREMIUM CORPORATE HERO SECTION WITH GLASSMORPHIC PANEL */}
        <section className="relative min-h-[92vh] flex items-center justify-center overflow-hidden border-b border-slate-800/80">
          {/* Architectural Background Image */}
          <div
            className="absolute inset-0 bg-cover bg-center bg-no-repeat transition-transform duration-1000 scale-100"
            style={{ backgroundImage: `url('/images/corporate-hq.jpg')` }}
            aria-hidden="true"
          />

          {/* Multi-layered Architectural Glass Darkening Overlays */}
          <div className="absolute inset-0 bg-slate-950/45 backdrop-brightness-[0.80]" aria-hidden="true" />
          <div
            className="absolute inset-0 bg-gradient-to-b from-slate-950/70 via-slate-950/30 to-slate-950/95"
            aria-hidden="true"
          />
          <div
            className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(15,23,42,0.3)_0%,rgba(2,6,23,0.85)_100%)]"
            aria-hidden="true"
          />

          {/* Hero Content Container */}
          <div className="relative z-10 mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
            {/* Architectural Glassmorphic Text Panel */}
            <div className="relative rounded-3xl border border-white/20 bg-slate-950/55 p-8 sm:p-12 md:p-16 text-center shadow-2xl shadow-black/80 backdrop-blur-2xl ring-1 ring-white/10 overflow-hidden">
              {/* Subtle Specular Glare along Top Glass Edge */}
              <div
                className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/40 to-transparent"
                aria-hidden="true"
              />

              {/* Corporate Enterprise Status Pill */}
              <div className="inline-flex items-center space-x-2.5 rounded-full border border-sky-400/30 bg-sky-950/40 px-4 py-1 text-xs font-semibold text-sky-200 mb-6 backdrop-blur-md shadow-inner">
                <span className="flex h-2 w-2 rounded-full bg-sky-400 animate-pulse"></span>
                <span>KNOWPATH Global Intelligence Platform</span>
                <span className="hidden sm:inline-block text-sky-400/60 font-light">|</span>
                <span className="hidden sm:inline-block text-slate-300 font-normal">Enterprise Edition v1.0</span>
              </div>

              {/* Main Heading */}
              <h1 className="text-3xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-[1.12]">
                Evidence-Based <br />
                <span className="bg-gradient-to-r from-sky-200 via-indigo-200 to-slate-100 bg-clip-text text-transparent">
                  Learner Intelligence
                </span>
              </h1>

              {/* Subheading */}
              <p className="mt-6 text-base sm:text-lg md:text-xl text-slate-200/90 max-w-2xl mx-auto leading-relaxed font-normal text-shadow">
                We model what learners demonstrably know, pinpoint exact prerequisite gaps across core programming
                foundations, and recommend the next high-leverage action—with every score mathematically explainable.
              </p>

              {/* High-Contrast Corporate CTA Buttons */}
              <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
                <Link
                  href="/register"
                  className="w-full sm:w-auto rounded-xl bg-gradient-to-r from-blue-600 via-indigo-600 to-indigo-700 px-8 py-3.5 text-base font-semibold text-white shadow-xl shadow-indigo-950/60 hover:from-blue-500 hover:to-indigo-600 border border-white/20 transition-all text-center group"
                >
                  <span className="flex items-center justify-center space-x-2">
                    <span>Start Free Adaptive Diagnostic</span>
                    <span className="group-hover:translate-x-1 transition-transform">→</span>
                  </span>
                </Link>
                <Link
                  href="/login"
                  className="w-full sm:w-auto rounded-xl border border-white/25 bg-white/10 hover:bg-white/15 px-8 py-3.5 text-base font-semibold text-white backdrop-blur-md transition-all text-center shadow-md hover:border-white/40"
                >
                  Sign In to Your Twin
                </Link>
              </div>

              {/* Integrated Corporate Metrics Grid */}
              <div className="mt-12 pt-8 border-t border-white/15 grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6 text-center">
                <div className="p-3">
                  <p className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">79</p>
                  <p className="mt-1 text-xs text-slate-300 font-medium uppercase tracking-wider">Python Concepts</p>
                </div>
                <div className="p-3">
                  <p className="text-2xl sm:text-3xl font-extrabold text-sky-300 tracking-tight">118</p>
                  <p className="mt-1 text-xs text-slate-300 font-medium uppercase tracking-wider">Prerequisite Edges</p>
                </div>
                <div className="p-3">
                  <p className="text-2xl sm:text-3xl font-extrabold text-teal-300 tracking-tight">430</p>
                  <p className="mt-1 text-xs text-slate-300 font-medium uppercase tracking-wider">Curated Questions</p>
                </div>
                <div className="p-3">
                  <p className="text-2xl sm:text-3xl font-extrabold text-indigo-300 tracking-tight">100%</p>
                  <p className="mt-1 text-xs text-slate-300 font-medium uppercase tracking-wider">Deterministic</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* 5 SIGNATURE INNOVATIONS */}
        <section className="py-20 md:py-28 bg-slate-950">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-3xl mx-auto mb-16">
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">The Architecture</span>
              <h2 className="mt-2 text-3xl sm:text-4xl font-extrabold text-white">Five Signature Innovations</h2>
              <p className="mt-4 text-slate-400 text-sm sm:text-base">
                Generic learning apps guess what you know with multiple-choice percentages. KNOWPATH models capability
                using Bayesian evidence updates, prerequisite graph theory, and verified safety constraints.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {/* Innovation 1 */}
              <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6 hover:border-indigo-500/50 transition-all">
                <div className="h-12 w-12 rounded-xl bg-indigo-950 border border-indigo-700/50 flex items-center justify-center text-2xl mb-4">
                  🧠
                </div>
                <h3 className="text-lg font-bold text-white">1. Cognitive Twin</h3>
                <p className="mt-2 text-sm text-slate-400 leading-relaxed">
                  A real-time probabilistic model of your knowledge state across 79 concepts. Every score maintains an
                  80% credible interval and transparent evidence provenance.
                </p>
                <div className="mt-4 pt-4 border-t border-slate-800 flex items-center text-xs text-indigo-400 font-semibold">
                  <span>Beta-distribution updating</span>
                  <span className="ml-1">→</span>
                </div>
              </div>

              {/* Innovation 2 */}
              <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6 hover:border-indigo-500/50 transition-all">
                <div className="h-12 w-12 rounded-xl bg-teal-950 border border-teal-700/50 flex items-center justify-center text-2xl mb-4">
                  🧬
                </div>
                <h3 className="text-lg font-bold text-white">2. Knowledge Genome</h3>
                <p className="mt-2 text-sm text-slate-400 leading-relaxed">
                  A cycle-free directed acyclic graph (DAG) mapping Python from variables and memory references to
                  metaclasses and generators with explicit prerequisites.
                </p>
                <div className="mt-4 pt-4 border-t border-slate-800 flex items-center text-xs text-teal-400 font-semibold">
                  <span>118 verified prerequisite edges</span>
                  <span className="ml-1">→</span>
                </div>
              </div>

              {/* Innovation 3 */}
              <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6 hover:border-indigo-500/50 transition-all">
                <div className="h-12 w-12 rounded-xl bg-sky-950 border border-sky-700/50 flex items-center justify-center text-2xl mb-4">
                  🎯
                </div>
                <h3 className="text-lg font-bold text-white">3. Adaptive Learning & Diagnostic</h3>
                <p className="mt-2 text-sm text-slate-400 leading-relaxed">
                  Our diagnostic engine computes information gain to present the exact item that minimizes uncertainty.
                  Distractors diagnose 34 common conceptual misconceptions.
                </p>
                <div className="mt-4 pt-4 border-t border-slate-800 flex items-center text-xs text-sky-400 font-semibold">
                  <span>34 tagged distractor traps</span>
                  <span className="ml-1">→</span>
                </div>
              </div>

              {/* Innovation 4 */}
              <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6 hover:border-indigo-500/50 transition-all">
                <div className="h-12 w-12 rounded-xl bg-purple-950 border border-purple-700/50 flex items-center justify-center text-2xl mb-4">
                  🔮
                </div>
                <h3 className="text-lg font-bold text-white">4. FuturePath Simulator</h3>
                <p className="mt-2 text-sm text-slate-400 leading-relaxed">
                  Simulate your capability against concrete professional requirements—such as Backend Web Services or
                  Data Pipelines—revealing unmastered prerequisite blockers.
                </p>
                <div className="mt-4 pt-4 border-t border-slate-800 flex items-center text-xs text-purple-400 font-semibold">
                  <span>Zero fake salary guarantees</span>
                  <span className="ml-1">→</span>
                </div>
              </div>

              {/* Innovation 5 */}
              <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6 hover:border-indigo-500/50 transition-all md:col-span-2">
                <div className="h-12 w-12 rounded-xl bg-amber-950 border border-amber-700/50 flex items-center justify-center text-2xl mb-4">
                  🤖
                </div>
                <h3 className="text-lg font-bold text-white">5. Collective Intelligence AI Orchestrator</h3>
                <p className="mt-2 text-sm text-slate-400 leading-relaxed">
                  Specialized agents collaborate through a central orchestrator with strict prompt safety filters:
                  Quality & Safety Agent blocks hallucinated career promises, teaching responses cite exact genome
                  sources, and all executions are audited with token-level cost accounting.
                </p>
                <div className="mt-4 pt-4 border-t border-slate-800 flex items-center text-xs text-amber-400 font-semibold">
                  <span>Audit-logged in agent_executions</span>
                  <span className="ml-1">→</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* INTERACTIVE EXPLAINER TABS */}
        <section className="py-20 bg-slate-900/40 border-y border-slate-800">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-12">
              <h2 className="text-2xl sm:text-3xl font-extrabold text-white">
                How Evidence-Based Scoring Actually Works
              </h2>
              <p className="mt-3 text-sm text-slate-400">
                Explore the deterministic formulas behind your Cognitive Twin.
              </p>
            </div>

            {/* Tab Controls */}
            <div className="flex flex-wrap justify-center gap-2 sm:gap-4 mb-8">
              <button
                onClick={() => setActiveTab("twin")}
                className={`px-4 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition-all cursor-pointer active:scale-95 select-none ${
                  activeTab === "twin"
                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/30"
                    : "bg-slate-900 text-slate-300 hover:text-white hover:bg-slate-800 border border-slate-800"
                }`}
              >
                Evidence Weighting
              </button>
              <button
                onClick={() => setActiveTab("genome")}
                className={`px-4 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition-all cursor-pointer active:scale-95 select-none ${
                  activeTab === "genome"
                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/30"
                    : "bg-slate-900 text-slate-300 hover:text-white hover:bg-slate-800 border border-slate-800"
                }`}
              >
                Prerequisite Graph Traversal
              </button>
              <button
                onClick={() => setActiveTab("scoring")}
                className={`px-4 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition-all cursor-pointer active:scale-95 select-none ${
                  activeTab === "scoring"
                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/30"
                    : "bg-slate-900 text-slate-300 hover:text-white hover:bg-slate-800 border border-slate-800"
                }`}
              >
                Beta Update & Recency Decay
              </button>
            </div>

            {/* Tab Content */}
            <div className="rounded-2xl border border-slate-800 bg-slate-950 p-6 sm:p-8 max-w-4xl mx-auto shadow-2xl">
              {activeTab === "twin" && (
                <div className="space-y-4">
                  <div className="flex items-center space-x-3 text-indigo-400">
                    <span className="text-xl">⚖️</span>
                    <h3 className="text-base font-bold text-white">Source Type Weight Hierarchy</h3>
                  </div>
                  <p className="text-sm text-slate-300 leading-relaxed">
                    Unlike ordinary platforms that equate a student checking a box to passing an exam, KnowPath assigns
                    fixed deterministic weights to each source type:
                  </p>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
                    <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                      <div className="text-xs text-slate-400 uppercase font-semibold">Self-Reported</div>
                      <div className="text-xl font-bold text-slate-200 mt-1">Weight: 0.10</div>
                      <p className="text-xs text-slate-500 mt-1">Initial user self-rating at onboarding</p>
                    </div>
                    <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                      <div className="text-xs text-amber-400 uppercase font-semibold">AI-Estimated</div>
                      <div className="text-xl font-bold text-amber-300 mt-1">Weight: 0.30</div>
                      <p className="text-xs text-slate-500 mt-1">Chat explanation & tutor interaction analysis</p>
                    </div>
                    <div className="p-4 rounded-xl bg-slate-900 border border-indigo-900/60 bg-indigo-950/20">
                      <div className="text-xs text-indigo-400 uppercase font-semibold">Assessment-Verified</div>
                      <div className="text-xl font-bold text-indigo-300 mt-1">Weight: 1.00</div>
                      <p className="text-xs text-slate-500 mt-1">Graded code reading, MCQ & predict-the-bug</p>
                    </div>
                  </div>
                  <p className="text-xs text-slate-400 pt-2 border-t border-slate-800/80">
                    Rule: Evidence sources are <strong>never upgraded implicitly</strong>. An assessment-verified signal
                    requires verified test execution.
                  </p>
                </div>
              )}

              {activeTab === "genome" && (
                <div className="space-y-4">
                  <div className="flex items-center space-x-3 text-teal-400">
                    <span className="text-xl">🌳</span>
                    <h3 className="text-base font-bold text-white">Prerequisite Gap & Foundation Bonus</h3>
                  </div>
                  <p className="text-sm text-slate-300 leading-relaxed">
                    When you set a target goal (e.g. &quot;Python for Placements&quot;), KnowPath runs topological
                    traversal across the Knowledge Genome DAG.
                  </p>
                  <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 text-xs font-mono text-slate-300 space-y-1">
                    <div>1. Compute missing concepts = Target Concepts \ Already Mastered (mastery &gt; 0.70)</div>
                    <div>2. Find transitive prerequisites for each unmastered target</div>
                    <div>3. Foundation bonus: Concepts that unblock 2+ downstream nodes receive a 1.25x priority boost</div>
                  </div>
                  <p className="text-xs text-slate-400">
                    Result: You never waste time memorizing advanced libraries before mastering mutability and variable
                    scope.
                  </p>
                </div>
              )}

              {activeTab === "scoring" && (
                <div className="space-y-4">
                  <div className="flex items-center space-x-3 text-sky-400">
                    <span className="text-xl">📐</span>
                    <h3 className="text-base font-bold text-white">Beta Distribution & 60-Day Recency Half-Life</h3>
                  </div>
                  <p className="text-sm text-slate-300 leading-relaxed">
                    Mastery is represented as a Beta probability distribution: Beta(alpha, beta).
                  </p>
                  <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 text-xs font-mono text-slate-300 space-y-1">
                    <div>Effective Weight = Source Weight × Recency Factor × Dispute Factor</div>
                    <div>Recency Factor = 0.5 ^ (days_elapsed / 60.0)</div>
                    <div>alpha = 1.0 + sum(effective_weight for correct responses)</div>
                    <div>beta  = 1.0 + sum(effective_weight for incorrect responses)</div>
                    <div>Mastery Score = alpha / (alpha + beta)</div>
                  </div>
                  <p className="text-xs text-slate-400">
                    Confidence reflects the 80% credible interval breadth: more recent, verified evidence narrows the
                    interval and increases confidence.
                  </p>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* CALL TO ACTION */}
        <section className="py-20 text-center">
          <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
              Ready to see what you <span className="text-indigo-400">actually</span> know?
            </h2>
            <p className="mt-4 text-slate-400 text-base max-w-xl mx-auto">
              No self-delusion. No hallucinated certificates. Take the 15-question adaptive diagnostic and construct
              your personal Cognitive Twin in 5 minutes.
            </p>
            <div className="mt-8 flex justify-center space-x-4">
              <Link
                href="/register"
                className="w-full sm:w-auto rounded-xl bg-indigo-600 px-8 py-3.5 text-base font-semibold text-white shadow-lg hover:bg-indigo-500 transition-all cursor-pointer active:scale-95 select-none inline-block"
              >
                Create Learner Account
              </Link>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
