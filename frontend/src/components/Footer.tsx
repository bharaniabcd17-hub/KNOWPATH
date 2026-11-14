import React from "react";
import Link from "next/link";

export default function Footer() {
  return (
    <footer className="border-t border-slate-800 bg-slate-950 text-slate-400">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-4">
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white p-0.5 shadow-md shadow-indigo-500/20 overflow-hidden border border-indigo-400/40 flex-shrink-0">
                <img src="/images/knowpath-logo.jpg" alt="KnowPath Logo" className="h-full w-full object-contain" />
              </div>
              <span className="text-lg font-bold text-white tracking-tight">KNOWPATH</span>
            </div>
            <p className="text-xs leading-relaxed text-slate-400">
              Evidence-based learner intelligence. We model what learners demonstrably know, identify missing
              foundations, and recommend the next high-leverage action—always explainably and with empirical proof.
            </p>
            <div className="inline-block rounded-md bg-slate-900 border border-slate-800 px-3 py-1.5 text-[11px] text-slate-400">
              🛡️ Deterministic Scoring • Zero Hallucinated Outcomes
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-200">Product Innovations</h3>
            <ul className="mt-4 space-y-2 text-sm">
              <li>
                <Link href="/features#cognitive-twin" className="hover:text-white transition-colors">
                  Cognitive Twin
                </Link>
              </li>
              <li>
                <Link href="/features#knowledge-genome" className="hover:text-white transition-colors">
                  Knowledge Genome
                </Link>
              </li>
              <li>
                <Link href="/features#adaptive-learning" className="hover:text-white transition-colors">
                  Adaptive Learning
                </Link>
              </li>
              <li>
                <Link href="/features#futurepath" className="hover:text-white transition-colors">
                  FuturePath Simulator
                </Link>
              </li>
              <li>
                <Link href="/features#collective-intelligence" className="hover:text-white transition-colors">
                  Collective Intelligence
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-200">Audience Solutions</h3>
            <ul className="mt-4 space-y-2 text-sm">
              <li>
                <Link href="/for-students" className="hover:text-white transition-colors">
                  College & Self-Learners
                </Link>
              </li>
              <li>
                <Link href="/for-professionals" className="hover:text-white transition-colors">
                  Software Engineers
                </Link>
              </li>
              <li>
                <Link href="/for-institutions" className="hover:text-white transition-colors">
                  Universities & Bootcamps
                </Link>
              </li>
              <li>
                <Link href="/how-it-works" className="hover:text-white transition-colors">
                  Evidence Architecture
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-200">Ethics & Compliance</h3>
            <ul className="mt-4 space-y-2 text-sm">
              <li>
                <Link href="/about#principles" className="hover:text-white transition-colors">
                  Explainability Charter
                </Link>
              </li>
              <li>
                <Link href="/about#privacy" className="hover:text-white transition-colors">
                  Data Sovereignty & GDPR
                </Link>
              </li>
              <li>
                <Link href="/contact" className="hover:text-white transition-colors">
                  Support & Audit Inquiries
                </Link>
              </li>
            </ul>
            <div className="mt-4 text-xs text-slate-500">
              Disclaimer: KnowPath makes no outcome guarantees (jobs, salaries, or grades). Mastery estimates reflect
              demonstrated assessment evidence.
            </div>
          </div>
        </div>

        <div className="mt-12 border-t border-slate-800/80 pt-6 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500">
          <p>© {new Date().getFullYear()} KNOWPATH / PROJECT-EVOLVE. All rights reserved.</p>
          <div className="mt-4 sm:mt-0 flex space-x-6">
            <span>Age Gate: 18+ Enforced</span>
            <span>Beta Distribution Engine v1.0</span>
            <span>FastAPI + Next.js</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
