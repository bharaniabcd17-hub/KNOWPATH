import React from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Link from "next/link";

export default function ForStudentsPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Navbar />

      <main className="flex-1 py-16 sm:py-24">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">Learners & College Students</span>
            <h1 className="mt-2 text-4xl sm:text-5xl font-extrabold text-white">Know Exactly Where You Stand</h1>
            <p className="mt-4 text-base sm:text-lg text-slate-400">
              Prepare for technical software assessments with zero guessing, zero fluff, and mathematically grounded
              capability models.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6 sm:p-8">
              <div className="text-2xl mb-3">🚫</div>
              <h3 className="text-lg font-bold text-white">The Typical Student Trap</h3>
              <p className="mt-2 text-sm text-slate-400 leading-relaxed">
                Watching 40 hours of Python video tutorials gives a false illusion of competence. In interviews,
                questions testing object references, mutable default arguments, or scope boundaries reveal glaring
                gaps.
              </p>
            </div>

            <div className="rounded-2xl border border-indigo-900/50 bg-indigo-950/20 p-6 sm:p-8">
              <div className="text-2xl mb-3">🎯</div>
              <h3 className="text-lg font-bold text-white">The KnowPath Difference</h3>
              <p className="mt-2 text-sm text-slate-300 leading-relaxed">
                We test code reading and bug prediction directly. When you make a mistake, our misconception detector
                explains <em>why</em> your mental model was flawed, pointing directly to the prerequisite concept to
                study.
              </p>
            </div>
          </div>

          <div className="mt-12 rounded-2xl border border-slate-800 bg-slate-900/40 p-8">
            <h3 className="text-xl font-bold text-white mb-4">What You Get as a Student</h3>
            <ul className="space-y-3 text-sm text-slate-300">
              <li className="flex items-center space-x-3">
                <span className="text-teal-400">✓</span>
                <span>Personalized Daily Missions (15-45 minutes) based on your weekly schedule</span>
              </li>
              <li className="flex items-center space-x-3">
                <span className="text-teal-400">✓</span>
                <span>Spaced review alerts before mastered concepts decay from memory</span>
              </li>
              <li className="flex items-center space-x-3">
                <span className="text-teal-400">✓</span>
                <span>AI Teaching Companion grounded strictly in verified curriculum notes</span>
              </li>
              <li className="flex items-center space-x-3">
                <span className="text-teal-400">✓</span>
                <span>Exportable JSON Capability Portfolio detailing verified assessment evidence</span>
              </li>
            </ul>
          </div>

          <div className="mt-16 text-center">
            <Link
              href="/register"
              className="w-full sm:w-auto inline-block rounded-xl bg-indigo-600 px-8 py-3.5 text-base font-semibold text-white shadow-lg shadow-indigo-600/30 hover:bg-indigo-500 transition-all cursor-pointer active:scale-95 select-none"
            >
              Sign Up as a Student
            </Link>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
