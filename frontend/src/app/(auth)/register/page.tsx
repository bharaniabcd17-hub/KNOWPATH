"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/stores/auth";
import Navbar from "@/components/Navbar";

export default function RegisterPage() {
  const router = useRouter();
  const { register } = useAuthStore();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [dob, setDob] = useState("");
  const [consentStorage, setConsentStorage] = useState(false);
  const [consentNoGuarantees, setConsentNoGuarantees] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const calculateAge = (birthDateString: string) => {
    const today = new Date();
    const birthDate = new Date(birthDateString);
    let age = today.getFullYear() - birthDate.getFullYear();
    const m = today.getMonth() - birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }
    return age;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Age validation
    if (!dob) {
      setError("Date of birth is required for age gate compliance.");
      return;
    }

    const age = calculateAge(dob);
    if (age < 18) {
      setError("Registration restricted: Users under 18 cannot register in Phase 1 per COPPA/GDPR rules.");
      return;
    }

    if (!consentStorage || !consentNoGuarantees) {
      setError("You must review and accept the explicit consent items to proceed.");
      return;
    }

    setLoading(true);

    try {
      await register({
        email,
        password,
        dob,
        consent_version: "1.0",
      });
      router.push("/dashboard");
    } catch (err: any) {
      setError(err?.message || "Registration failed. Please check your details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Navbar />

      <main className="flex-1 flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-lg rounded-2xl border border-slate-800 bg-slate-900/60 p-8 shadow-2xl backdrop-blur-sm">
          <div className="text-center mb-6">
            <div className="inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-white p-1 mb-3 shadow-xl shadow-indigo-600/30 border border-indigo-400/40 overflow-hidden">
              <img src="/images/knowpath-logo.jpg" alt="KnowPath Logo" className="h-full w-full object-contain" />
            </div>
            <h1 className="text-2xl font-bold text-white tracking-tight">Create Learner Account</h1>
            <p className="mt-1 text-xs text-slate-400">
              Evidence-based learner modeling with verified date-of-birth compliance
            </p>
          </div>

          {error && (
            <div className="mb-5 rounded-lg border border-rose-900/50 bg-rose-950/40 p-3 text-xs text-rose-300">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
                Email Address
              </label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="learner@domain.edu"
                className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3.5 py-2.5 text-sm text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5 block">
                Password
              </label>
              <input
                type="password"
                required
                minLength={8}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Minimum 8 characters"
                className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3.5 py-2.5 text-sm text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
            </div>

            {/* Age Gate DOB */}
            <div>
              <div className="flex justify-between items-center mb-1.5">
                <label className="text-xs font-semibold uppercase tracking-wider text-slate-300">
                  Date of Birth (18+ Age Gate)
                </label>
                <span className="text-[10px] text-indigo-400 font-medium">Phase 1 Requirement</span>
              </div>
              <input
                type="date"
                required
                value={dob}
                onChange={(e) => setDob(e.target.value)}
                className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3.5 py-2.5 text-sm text-white focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
              <p className="mt-1 text-[11px] text-slate-500">
                Phase 1 is strictly restricted to learners aged 18 and older. Minor support will be introduced in a
                later phase.
              </p>
            </div>

            {/* Explicit Consent Box */}
            <div className="pt-2">
              <label className="text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2 block">
                Explicit Consent & Platform Terms
              </label>
              <div className="rounded-xl border border-slate-800 bg-slate-950 p-3.5 space-y-3 text-xs text-slate-300">
                <label className="flex items-start space-x-2.5 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={consentStorage}
                    onChange={(e) => setConsentStorage(e.target.checked)}
                    className="mt-0.5 rounded border-slate-700 bg-slate-900 text-indigo-600 focus:ring-0"
                  />
                  <span className="leading-snug">
                    I consent to KNOWPATH storing my assessment answers, timestamp evidence, and calculating my
                    probabilistic Cognitive Twin.
                  </span>
                </label>

                <label className="flex items-start space-x-2.5 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={consentNoGuarantees}
                    onChange={(e) => setConsentNoGuarantees(e.target.checked)}
                    className="mt-0.5 rounded border-slate-700 bg-slate-900 text-indigo-600 focus:ring-0"
                  />
                  <span className="leading-snug">
                    I acknowledge that mastery scores are calculated deterministically and that KNOWPATH provides no
                    outcome guarantees (jobs, salaries, or grades).
                  </span>
                </label>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full mt-2 rounded-xl bg-indigo-600 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-600/30 hover:bg-indigo-500 disabled:opacity-50 transition-all cursor-pointer active:scale-98 select-none"
            >
              {loading ? "Creating Account..." : "Create Account & Enter Platform"}
            </button>
          </form>

          <div className="mt-6 pt-6 border-t border-slate-800 text-center text-xs text-slate-400">
            Already registered?{" "}
            <Link href="/login" className="text-indigo-400 font-semibold hover:underline">
              Sign in to your account
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}
