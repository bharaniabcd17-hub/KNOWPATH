import React from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Link from "next/link";

export default function HowItWorksPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Navbar />

      <main className="flex-1 py-16 sm:py-24">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">Step-by-Step Flow</span>
            <h1 className="mt-2 text-4xl sm:text-5xl font-extrabold text-white">How KNOWPATH Works</h1>
            <p className="mt-4 text-base sm:text-lg text-slate-400">
              From onboarding to verifiable capability proof: a continuous, mathematically rigorous loop.
            </p>
          </div>

          <div className="space-y-12 relative before:absolute before:inset-0 before:left-8 before:w-0.5 before:bg-slate-800 before:hidden md:before:block">
            {/* Step 1 */}
            <div className="relative flex flex-col md:flex-row items-start md:space-x-8 rounded-2xl border border-slate-800 bg-slate-900/40 p-6 sm:p-8">
              <div className="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-xl bg-indigo-600 font-bold text-white text-lg mb-4 md:mb-0">
                1
              </div>
              <div>
                <h3 className="text-xl font-bold text-white">Age Verification & Explicit Consent</h3>
                <p className="mt-2 text-sm text-slate-300 leading-relaxed">
                  You complete the date-of-birth age gate (18+ only in Phase 1) and inspect our explicit consent screen
                  detailing exactly what evidence is captured and how your model evolves.
                </p>
              </div>
            </div>

            {/* Step 2 */}
            <div className="relative flex flex-col md:flex-row items-start md:space-x-8 rounded-2xl border border-slate-800 bg-slate-900/40 p-6 sm:p-8">
              <div className="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-xl bg-teal-600 font-bold text-white text-lg mb-4 md:mb-0">
                2
              </div>
              <div>
                <h3 className="text-xl font-bold text-white">Adaptive Diagnostic Assessment</h3>
                <p className="mt-2 text-sm text-slate-300 leading-relaxed">
                  Take a 15-item adaptive assessment. Rather than random questions, our information-gain selector serves
                  items at your knowledge frontier to calibrate your baseline across core Python concepts.
                </p>
              </div>
            </div>

            {/* Step 3 */}
            <div className="relative flex flex-col md:flex-row items-start md:space-x-8 rounded-2xl border border-slate-800 bg-slate-900/40 p-6 sm:p-8">
              <div className="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-xl bg-sky-600 font-bold text-white text-lg mb-4 md:mb-0">
                3
              </div>
              <div>
                <h3 className="text-xl font-bold text-white">Cognitive Twin Instantiation</h3>
                <p className="mt-2 text-sm text-slate-300 leading-relaxed">
                  Your responses immediately update your Cognitive Twin. Each concept receives a Beta distribution
                  mastery score, credible interval, and transparent evidence trail.
                </p>
              </div>
            </div>

            {/* Step 4 */}
            <div className="relative flex flex-col md:flex-row items-start md:space-x-8 rounded-2xl border border-slate-800 bg-slate-900/40 p-6 sm:p-8">
              <div className="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-xl bg-purple-600 font-bold text-white text-lg mb-4 md:mb-0">
                4
              </div>
              <div>
                <h3 className="text-xl font-bold text-white">Topological Gap Detection & Roadmap</h3>
                <p className="mt-2 text-sm text-slate-300 leading-relaxed">
                  Choose your target goal (&quot;Python for Placements&quot; or &quot;Python for Data Work&quot;). Our
                  gap engine traverses the DAG to output an ordered roadmap with foundation bonuses for concepts that
                  unblock downstream dependencies.
                </p>
              </div>
            </div>

            {/* Step 5 */}
            <div className="relative flex flex-col md:flex-row items-start md:space-x-8 rounded-2xl border border-slate-800 bg-slate-900/40 p-6 sm:p-8">
              <div className="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-xl bg-amber-600 font-bold text-white text-lg mb-4 md:mb-0">
                5
              </div>
              <div>
                <h3 className="text-xl font-bold text-white">Daily Missions & Spaced Revision</h3>
                <p className="mt-2 text-sm text-slate-300 leading-relaxed">
                  Receive a focused 15-45 min daily mission tailored to your available hours, reinforced by an SM-2
                  spaced retention schedule so acquired concepts don&apos;t decay.
                </p>
              </div>
            </div>
          </div>

          <div className="mt-16 text-center">
            <Link
              href="/register"
              className="w-full sm:w-auto inline-block rounded-xl bg-indigo-600 px-8 py-3.5 text-base font-semibold text-white shadow-lg shadow-indigo-600/30 hover:bg-indigo-500 transition-all cursor-pointer active:scale-95 select-none"
            >
              Start the Process Now
            </Link>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
