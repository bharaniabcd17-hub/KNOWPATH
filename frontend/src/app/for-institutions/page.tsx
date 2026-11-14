import React from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Link from "next/link";

export default function ForInstitutionsPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Navbar />

      <main className="flex-1 py-16 sm:py-24">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">Institutions & Universities</span>
            <h1 className="mt-2 text-4xl sm:text-5xl font-extrabold text-white">Auditable Learner Analytics</h1>
            <p className="mt-4 text-base sm:text-lg text-slate-400">
              Replace subjective grading curves with an evidence-backed cognitive model across entire cohorts.
            </p>
          </div>

          <div className="space-y-8">
            <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6 sm:p-8">
              <h3 className="text-xl font-bold text-white mb-2">Cohort Misconception Clustering</h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                Discover which prerequisite concepts are systematically failing across your student body. If 64% of
                students trigger <code className="text-indigo-400">MISCON_MUTABLE_DEFAULT</code>, instructors can immediately adapt lecture
                curricula before exam season.
              </p>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6 sm:p-8">
              <h3 className="text-xl font-bold text-white mb-2">Total AI Auditability & Cost Control</h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                Every AI interaction is traced in <code className="text-indigo-400">agent_executions</code> with prompt tokens, completion
                tokens, model latency, and deterministic safety checks. No hidden external API calls or hallucinated
                grading.
              </p>
            </div>
          </div>

          <div className="mt-16 text-center">
            <Link
              href="/contact"
              className="w-full sm:w-auto inline-block rounded-xl bg-indigo-600 px-8 py-3.5 text-base font-semibold text-white shadow-lg shadow-indigo-600/30 hover:bg-indigo-500 transition-all cursor-pointer active:scale-95 select-none"
            >
              Contact Our Institutional Team
            </Link>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
