"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { MissionRead } from "@/types";

export default function MissionsPage() {
  const [mission, setMission] = useState<MissionRead | null>(null);
  const [loading, setLoading] = useState(true);
  const [completing, setCompleting] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);

  const fetchMission = async () => {
    try {
      setLoading(true);
      const data = await api.getTodayMission();
      setMission(data);
    } catch (err) {
      console.error("Mission fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMission();
  }, []);

  const handleComplete = async () => {
    if (!mission) return;
    try {
      setCompleting(true);
      await api.completeMission(mission.id);
      setMsg("Mission marked complete! Evidence logged to your Cognitive Twin.");
      fetchMission();
    } catch (err: any) {
      setMsg(`Error: ${err?.message || "Failed to complete mission"}`);
    } finally {
      setCompleting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="flex items-center space-x-3 text-slate-400">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent"></div>
          <span className="text-sm">Preparing today&apos;s adaptive mission...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-4xl">
      {/* Header */}
      <div className="border-b border-slate-800 pb-6">
        <div className="inline-flex items-center space-x-2 rounded-full bg-indigo-950/80 border border-indigo-700/50 px-3 py-0.5 text-xs font-semibold text-indigo-300 mb-2">
          <span>Micro-Learning Cadence</span>
        </div>
        <h1 className="text-3xl font-extrabold text-white">Daily Missions</h1>
        <p className="mt-1 text-sm text-slate-400">
          Targeted 15-45 minute daily micro-tasks calibrated to your available hours and active knowledge gaps.
        </p>
      </div>

      {mission ? (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 sm:p-8 space-y-6">
          <div className="flex items-center justify-between pb-4 border-b border-slate-800">
            <div>
              <span className="text-xs text-indigo-400 font-semibold uppercase tracking-wider">
                Today&apos;s Focus
              </span>
              <h2 className="text-xl font-bold text-white mt-1">{mission.title}</h2>
            </div>
            <span className="rounded-lg bg-indigo-950 border border-indigo-800 px-3 py-1 text-xs font-bold text-indigo-300">
              ⏱️ {mission.estimated_minutes} min
            </span>
          </div>

          <p className="text-sm text-slate-300 leading-relaxed">{mission.description}</p>

          {/* Action Steps */}
          <div className="space-y-3 pt-2">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">Mission Steps</h3>

            {mission.reading_url && (
              <div className="p-4 rounded-xl border border-slate-800 bg-slate-950 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div className="flex items-center space-x-3">
                  <span className="text-lg">📖</span>
                  <div>
                    <h4 className="text-xs font-bold text-white">Step 1: Concept Reading</h4>
                    <p className="text-[11px] text-slate-400">Review notes and code examples in the Genome</p>
                  </div>
                </div>
                <Link
                  href={mission.reading_url}
                  className="w-full sm:w-auto text-center rounded-lg bg-indigo-600 px-4 py-2 text-xs font-semibold text-white hover:bg-indigo-500 transition-all cursor-pointer active:scale-95 select-none"
                >
                  Open Study Notes →
                </Link>
              </div>
            )}

            <div className="p-4 rounded-xl border border-slate-800 bg-slate-950 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div className="flex items-center space-x-3">
                <span className="text-lg">🎯</span>
                <div>
                  <h4 className="text-xs font-bold text-white">Step 2: Retrieval Practice</h4>
                  <p className="text-[11px] text-slate-400">Answer 3-5 quick diagnostic questions on this topic</p>
                </div>
              </div>
              <Link
                href="/assessment/diagnostic"
                className="w-full sm:w-auto text-center rounded-lg bg-teal-600 px-4 py-2 text-xs font-semibold text-white hover:bg-teal-500 transition-all cursor-pointer active:scale-95 select-none"
              >
                Start Practice →
              </Link>
            </div>
          </div>

          {msg && (
            <div className="p-3 rounded-lg bg-emerald-950/40 border border-emerald-900/60 text-xs text-emerald-300">
              {msg}
            </div>
          )}

          {/* Footer Action */}
          <div className="pt-4 border-t border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="text-xs text-slate-400">
              Status:{" "}
              <span className={`font-semibold ${mission.completed ? "text-emerald-400" : "text-amber-400"}`}>
                {mission.completed ? "✓ Completed for today" : "In Progress"}
              </span>
            </div>

            {!mission.completed && (
              <button
                onClick={handleComplete}
                disabled={completing}
                className="w-full sm:w-auto rounded-xl bg-indigo-600 px-5 py-2.5 text-xs font-semibold text-white hover:bg-indigo-500 disabled:opacity-50 transition-all cursor-pointer active:scale-95 select-none"
              >
                {completing ? "Recording evidence..." : "Complete & Log Evidence"}
              </button>
            )}
          </div>
        </div>
      ) : (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-12 text-center text-slate-400">
          <p>No active mission assigned for today.</p>
        </div>
      )}
    </div>
  );
}
