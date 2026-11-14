import React from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Link from "next/link";

export default function ForProfessionalsPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Navbar />

      <main className="flex-1 py-16 sm:py-24">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">Software Professionals</span>
            <h1 className="mt-2 text-4xl sm:text-5xl font-extrabold text-white">Targeted Knowledge Remediation</h1>
            <p className="mt-4 text-base sm:text-lg text-slate-400">
              Skip what you already know. Target high-leverage edge cases, decorators, generators, and memory semantics.
            </p>
          </div>

          <div className="space-y-8">
            <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6 sm:p-8">
              <h3 className="text-xl font-bold text-white mb-2">Diagnostic Skip-Ahead</h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                Experienced engineers don&apos;t need to re-learn what a loop is. Our information-gain item selection
                quickly moves past basic syntax to evaluate advanced concepts: context managers, closures, generator
                pipelines, and exception hierarchies.
              </p>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6 sm:p-8">
              <h3 className="text-xl font-bold text-white mb-2">Verifiable Capability Proof</h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                Provide verifiable evidence of language mastery for internal promotions or technical transitions. All
                evaluations are anchored to timestamped test events, difficulty tiers, and misconception resistance.
              </p>
            </div>
          </div>

          <div className="mt-16 text-center">
            <Link
              href="/register"
              className="w-full sm:w-auto inline-block rounded-xl bg-indigo-600 px-8 py-3.5 text-base font-semibold text-white shadow-lg shadow-indigo-600/30 hover:bg-indigo-500 transition-all cursor-pointer active:scale-95 select-none"
            >
              Verify Professional Capabilities
            </Link>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
