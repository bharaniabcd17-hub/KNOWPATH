"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { useAuthStore } from "@/stores/auth";
import { GoalKey, Profile } from "@/types";

export default function SettingsPage() {
  const router = useRouter();
  const { user, logout } = useAuthStore();

  const [profile, setProfile] = useState<Profile | null>(null);
  const [weeklyHours, setWeeklyHours] = useState<number>(5);
  const [explanationStyle, setExplanationStyle] = useState<string>("intuitive");
  const [targetGoal, setTargetGoal] = useState<GoalKey>("python_placements");
  const [saving, setSaving] = useState(false);
  const [exporting, setExporting] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState("");
  const [deleting, setDeleting] = useState(false);
  const [saveMsg, setSaveMsg] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const p = await api.getProfile();
        setProfile(p);
        if (p.weekly_hours) setWeeklyHours(p.weekly_hours);
        if (p.explanation_style) setExplanationStyle(p.explanation_style);
      } catch (err) {
        console.error("Profile load error:", err);
      }
    };
    load();
  }, []);

  const handleSavePreferences = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSaving(true);
      await api.updateProfile({
        weekly_hours: weeklyHours,
        explanation_style: explanationStyle as any,
      });
      await api.createGoal(targetGoal);
      setSaveMsg("Preferences updated successfully!");
    } catch (err: any) {
      setSaveMsg(`Error: ${err?.message || "Failed to update profile"}`);
    } finally {
      setSaving(false);
    }
  };

  const handleExportData = async () => {
    try {
      setExporting(true);
      const blob = await api.exportData();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `knowpath_user_export_${new Date().toISOString().split("T")[0]}.json`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err: any) {
      alert(`Export error: ${err?.message || "Failed to export data"}`);
    } finally {
      setExporting(false);
    }
  };

  const handleDeleteAccount = async () => {
    if (deleteConfirm !== "DELETE") {
      alert("Please type 'DELETE' in uppercase to confirm account deletion.");
      return;
    }

    if (!confirm("Are you strictly sure? All Cognitive Twin estimates and test evidence will be permanently erased.")) {
      return;
    }

    try {
      setDeleting(true);
      await api.deleteAccount("DELETE");
      await logout();
      router.push("/");
    } catch (err: any) {
      alert(`Account deletion failed: ${err?.message || "Error"}`);
    } finally {
      setDeleting(false);
    }
  };

  return (
    <div className="space-y-8 max-w-4xl">
      {/* Header */}
      <div className="border-b border-slate-800 pb-6">
        <h1 className="text-3xl font-extrabold text-white">Settings & Privacy</h1>
        <p className="mt-1 text-sm text-slate-400">
          Manage your learning cadence, target goals, data sovereignty exports, and account deletion.
        </p>
      </div>

      {saveMsg && (
        <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-200">
          {saveMsg}
        </div>
      )}

      {/* Official Profile Picture & Identity Card */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 sm:p-8 flex flex-col sm:flex-row items-center sm:items-start gap-6">
        <div className="relative h-24 w-24 rounded-2xl bg-white p-1.5 border-2 border-indigo-500/50 shadow-xl shadow-indigo-600/20 overflow-hidden flex-shrink-0">
          <img
            src="/images/knowpath-avatar.jpg"
            alt="Official Website Profile Picture"
            className="h-full w-full rounded-xl object-cover"
          />
          <span className="absolute bottom-1 right-1 h-3.5 w-3.5 rounded-full bg-emerald-500 border-2 border-slate-950" title="Active learner"></span>
        </div>
        <div className="flex-1 text-center sm:text-left space-y-2">
          <div className="flex flex-wrap items-center justify-center sm:justify-start gap-2">
            <h2 className="text-xl font-bold text-white">{user?.email || "Learner Account"}</h2>
            <span className="rounded-full bg-indigo-500/20 border border-indigo-500/40 px-2.5 py-0.5 text-xs font-semibold text-indigo-300">
              Verified Learner
            </span>
            <span className="rounded-full bg-emerald-500/20 border border-emerald-500/40 px-2.5 py-0.5 text-xs font-semibold text-emerald-300">
              Official Avatar Active
            </span>
          </div>
          <p className="text-xs text-slate-400 max-w-xl">
            Your official KnowPath profile picture represents your Cognitive Twin identity across adaptive roadmaps, diagnostic assessments, and verifiable capability portfolios.
          </p>
          <div className="pt-1 flex flex-wrap items-center justify-center sm:justify-start gap-2 text-xs text-slate-400">
            <span className="inline-flex items-center px-2.5 py-1 rounded-md bg-slate-950 border border-slate-800">
              🛡️ Age Gate Verified (18+)
            </span>
            <span className="inline-flex items-center px-2.5 py-1 rounded-md bg-slate-950 border border-slate-800">
              📊 Provenance: Deterministic
            </span>
          </div>
        </div>
      </div>

      {/* Profile & Learning Preferences Form */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 sm:p-8">
        <h2 className="text-lg font-bold text-white mb-4">Learning Preferences</h2>
        <form onSubmit={handleSavePreferences} className="space-y-5">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
                Target Learning Goal
              </label>
              <select
                value={targetGoal}
                onChange={(e) => setTargetGoal(e.target.value as GoalKey)}
                className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3.5 py-2.5 text-xs text-white focus:border-indigo-500 focus:outline-none"
              >
                <option value="python_placements">Python for Placements & Coding Interviews</option>
                <option value="python_data">Python for Data Analysis & Engineering</option>
                <option value="python_basics">Python Fundamentals & Syntax</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
                Weekly Available Study Hours
              </label>
              <input
                type="number"
                min={1}
                max={40}
                value={weeklyHours}
                onChange={(e) => setWeeklyHours(parseInt(e.target.value) || 1)}
                className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3.5 py-2.5 text-xs text-white focus:border-indigo-500 focus:outline-none"
              />
              <span className="text-[10px] text-slate-500 mt-1 block">
                Adjusts duration of your Daily Missions (15 to 45 min).
              </span>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
              AI Explanation Style
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {[
                { id: "intuitive", label: "Intuitive & Visual", desc: "Mental models and real-world analogies" },
                { id: "formal", label: "Formal & Rigorous", desc: "Language specifications and exact rules" },
                { id: "code_first", label: "Code-First", desc: "Minimal prose, concrete runnable snippets" },
              ].map((style) => (
                <button
                  type="button"
                  key={style.id}
                  onClick={() => setExplanationStyle(style.id)}
                  className={`p-3 rounded-xl border text-left transition-all cursor-pointer active:scale-98 select-none ${
                    explanationStyle === style.id
                      ? "border-indigo-500 bg-indigo-950/40 text-white shadow-sm"
                      : "border-slate-800 bg-slate-950 text-slate-400 hover:border-slate-700"
                  }`}
                >
                  <div className="text-xs font-bold">{style.label}</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">{style.desc}</div>
                </button>
              ))}
            </div>
          </div>

          <button
            type="submit"
            disabled={saving}
            className="w-full sm:w-auto rounded-xl bg-indigo-600 px-6 py-2.5 text-xs font-semibold text-white hover:bg-indigo-500 disabled:opacity-50 transition-all cursor-pointer active:scale-95 select-none"
          >
            {saving ? "Saving..." : "Save Preferences"}
          </button>
        </form>
      </div>

      {/* GDPR Data Export */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 sm:p-8">
        <h2 className="text-lg font-bold text-white mb-2">Data Sovereignty & Export (GDPR Article 20)</h2>
        <p className="text-xs text-slate-400 mb-4 leading-relaxed">
          Download a complete, machine-readable JSON archive of your personal profile, Cognitive Twin parameters,
          historical evidence logs, and assessment scores.
        </p>
        <button
          onClick={handleExportData}
          disabled={exporting}
          className="w-full sm:w-auto rounded-xl border border-slate-700 bg-slate-950 px-5 py-2.5 text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-900 transition-all cursor-pointer active:scale-95 select-none"
        >
          {exporting ? "Compiling JSON Export..." : "Download Data Archive (.json)"}
        </button>
      </div>

      {/* Account Deletion (Danger Zone) */}
      <div className="rounded-2xl border border-rose-950 bg-rose-950/10 p-6 sm:p-8">
        <h2 className="text-lg font-bold text-rose-400 mb-2">Delete Account (Right to Erasure)</h2>
        <p className="text-xs text-slate-400 mb-4 leading-relaxed">
          Hard account deletion immediately wipes your account, profile, Cognitive Twin parameters, and assessment
          evidence from our databases. This action is irrevocable.
        </p>

        <div className="space-y-3 max-w-sm">
          <label className="text-[11px] text-slate-400 block">
            Type <strong className="text-rose-400">DELETE</strong> to confirm:
          </label>
          <input
            type="text"
            value={deleteConfirm}
            onChange={(e) => setDeleteConfirm(e.target.value)}
            placeholder="DELETE"
            className="w-full rounded-lg border border-rose-900/60 bg-slate-950 px-3.5 py-2 text-xs text-white focus:border-rose-500 focus:outline-none"
          />
          <button
            onClick={handleDeleteAccount}
            disabled={deleting || deleteConfirm !== "DELETE"}
            className="w-full rounded-xl bg-rose-600 py-3 text-xs font-semibold text-white hover:bg-rose-500 disabled:opacity-40 transition-all cursor-pointer active:scale-98 select-none"
          >
            {deleting ? "Deleting Account..." : "Permanently Delete My Account"}
          </button>
        </div>
      </div>
    </div>
  );
}
