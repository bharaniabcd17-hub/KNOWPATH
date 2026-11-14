import React from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Link from "next/link";

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Navbar />

      <main className="flex-1 py-16 sm:py-24">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">Our Mission</span>
            <h1 className="mt-2 text-4xl sm:text-5xl font-extrabold text-white">About KNOWPATH</h1>
            <p className="mt-4 text-base sm:text-lg text-slate-400 max-w-2xl mx-auto">
              KNOWPATH / PROJECT-EVOLVE was founded on a simple principle: human capability development must be grounded
              in demonstrable evidence, transparent mathematics, and total user agency.
            </p>
          </div>

          <div className="space-y-12 text-slate-300 leading-relaxed text-sm sm:text-base">
            <section className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6 sm:p-8">
              <h2 className="text-2xl font-bold text-white mb-4">The Problem with Traditional EdTech</h2>
              <p>
                Modern online education relies almost universally on passive video completion rates, vanity streaks,
                and self-assessed confidence. Meanwhile, generative AI chatbots answer questions enthusiastically but
                often hallucinate capabilities that learners do not actually possess.
              </p>
              <p className="mt-3">
                When candidates enter technical interviews or production environments, missing foundational concepts
                lead to immediate failure and frustration.
              </p>
            </section>

            <section className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6 sm:p-8" id="principles">
              <h2 className="text-2xl font-bold text-white mb-4">Our Non-Negotiable Charter</h2>
              <ul className="space-y-4">
                <li className="flex items-start space-x-3">
                  <span className="text-indigo-400 text-lg">✓</span>
                  <div>
                    <strong className="text-white">Deterministic Scoring:</strong> LLMs paraphrase concepts and tutor
                    learners, but <em>never</em> calculate mastery scores. Scores derive from closed-form Bayesian Beta
                    distribution updates.
                  </div>
                </li>
                <li className="flex items-start space-x-3">
                  <span className="text-indigo-400 text-lg">✓</span>
                  <div>
                    <strong className="text-white">Strict Evidence Hierarchy:</strong> Self-reports are never upgraded
                    to assessment proof without genuine test execution.
                  </div>
                </li>
                <li className="flex items-start space-x-3">
                  <span className="text-indigo-400 text-lg">✓</span>
                  <div>
                    <strong className="text-white">No Outcome Guarantees:</strong> We never promise jobs, salaries, or
                    grade outcomes. We measure demonstrated knowledge with rigorous confidence intervals.
                  </div>
                </li>
                <li className="flex items-start space-x-3">
                  <span className="text-indigo-400 text-lg">✓</span>
                  <div>
                    <strong className="text-white">Right of Dispute:</strong> If an assessment question or score is
                    contested, learners can file an auditable dispute directly in the app.
                  </div>
                </li>
              </ul>
            </section>

            <section className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6 sm:p-8" id="privacy">
              <h2 className="text-2xl font-bold text-white mb-4">Data Sovereignty & Age Protection</h2>
              <p>
                In compliance with global data protection principles and COPPA/GDPR age rules, KNOWPATH enforces a
                strict age gate requiring users to be 18 or older during Phase 1.
              </p>
              <p className="mt-3">
                All learners possess full export rights (JSON machine-readable archive) and hard account deletion rights
                with complete cryptographic wipe of personal records.
              </p>
            </section>
          </div>

          <div className="mt-16 text-center">
            <Link
              href="/register"
              className="w-full sm:w-auto inline-block rounded-xl bg-indigo-600 px-8 py-3.5 text-base font-semibold text-white shadow-lg shadow-indigo-600/30 hover:bg-indigo-500 transition-all cursor-pointer active:scale-95 select-none"
            >
              Get Started with KNOWPATH
            </Link>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
