"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { MissionRead, ReviewItem, TwinPageData } from "@/types";

export default function DashboardOverview() {
  const [twin, setTwin] = useState<TwinPageData | null>(null);
  const [mission, setMission] = useState<MissionRead | null>(null);
  const [dueReviews, setDueReviews] = useState<ReviewItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [completingMission, setCompletingMission] = useState(false);
  const [missionDoneMsg, setMissionDoneMsg] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [twinData, missionData, reviewsData] = await Promise.allSettled([
        api.getTwin(),
        api.getTodayMission(),
        api.getDueReviews(),
      ]);

      if (twinData.status === "fulfilled") setTwin(twinData.value);
      if (missionData.status === "fulfilled") setMission(missionData.value);
      if (reviewsData.status === "fulfilled") setDueReviews(reviewsData.value);
    } catch (err) {
      console.error("Dashboard fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleCompleteMission = async () => {
    if (!mission) return;
    setCompletingMission(true);
    try {
      await api.completeMission(mission.id);
      setMissionDoneMsg("Mission completed! Evidence logged to Cognitive Twin.");
      fetchData();
    } catch (err: any) {
      setMissionDoneMsg(`Failed: ${err?.message || "Unknown error"}`);
    } finally {
      setCompletingMission(false);
    }
  };

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="flex items-center space-x-3 text-slate-400">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent"></div>
          <span className="text-sm">Calibrating your learner intelligence data...</span>
        </div>
      </div>
    );
  }

  const masteredCount = twin?.mastery_list?.filter((m) => m.mastery_score >= 0.7).length || 0;
  const inProgressCount = twin?.mastery_list?.filter((m) => m.mastery_score >= 0.3 && m.mastery_score < 0.7).length || 0;
  const totalConcepts = twin?.mastery_list?.length || 79;
  const avgMastery =
    twin?.mastery_list && twin.mastery_list.length > 0
      ? (twin.mastery_list.reduce((acc, curr) => acc + curr.mastery_score, 0) / twin.mastery_list.length) * 100
      : 0;

  return (
    <div className="space-y-8">
      {/* Top Banner / Welcome */}
      <div className="rounded-2xl border border-slate-800 bg-gradient-to-r from-slate-900 via-indigo-950/30 to-slate-900 p-6 sm:p-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center space-x-2 rounded-full bg-indigo-950/80 border border-indigo-700/50 px-3 py-0.5 text-xs font-semibold text-indigo-300 mb-2">
              <span>Goal: Python for Placements</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white">Learner Intelligence Overview</h1>
            <p className="mt-1 text-sm text-slate-400">
              Your model is calibrated against 79 Python concepts using Beta distribution updates and evidence decay.
            </p>
          </div>
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2.5 sm:gap-3">
            <Link
              href="/assessment/diagnostic"
              className="rounded-xl bg-indigo-600 px-5 py-2.5 text-xs sm:text-sm font-semibold text-white shadow-md hover:bg-indigo-500 transition-all text-center cursor-pointer active:scale-95 select-none"
            >
              Take Adaptive Diagnostic
            </Link>
            <Link
              href="/twin"
              className="rounded-xl border border-slate-700 bg-slate-900 px-4 py-2.5 text-xs sm:text-sm font-semibold text-slate-300 hover:text-white hover:bg-slate-800 transition-all text-center cursor-pointer active:scale-95 select-none"
            >
              Inspect Twin
            </Link>
          </div>
        </div>
      </div>

      {/* Primary Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Mastered Concepts</span>
            <span className="text-base">🏆</span>
          </div>
          <div className="mt-3 flex items-baseline space-x-2">
            <span className="text-3xl font-bold text-white">{masteredCount}</span>
            <span className="text-xs text-slate-400">/ {totalConcepts}</span>
          </div>
          <div className="mt-2 text-xs text-emerald-400">Score &ge; 0.70 demonstrated</div>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">In Progress</span>
            <span className="text-base">⏳</span>
          </div>
          <div className="mt-3 flex items-baseline space-x-2">
            <span className="text-3xl font-bold text-indigo-400">{inProgressCount}</span>
            <span className="text-xs text-slate-400">concepts</span>
          </div>
          <div className="mt-2 text-xs text-indigo-300">Frontier calibration active</div>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Avg Model Score</span>
            <span className="text-base">📐</span>
          </div>
          <div className="mt-3 flex items-baseline space-x-2">
            <span className="text-3xl font-bold text-white">{avgMastery.toFixed(1)}%</span>
          </div>
          <div className="mt-2 text-xs text-slate-400">Beta posterior mean</div>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Due Reviews</span>
            <span className="text-base">🔄</span>
          </div>
          <div className="mt-3 flex items-baseline space-x-2">
            <span className="text-3xl font-bold text-amber-400">{dueReviews.length}</span>
            <span className="text-xs text-slate-400">items</span>
          </div>
          <div className="mt-2 text-xs text-amber-300/80">SM-2 memory retention queue</div>
        </div>
      </div>

      {/* Main Two-Column Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Today's Mission & Roadmap Snapshot */}
        <div className="lg:col-span-2 space-y-6">
          {/* Mission Card */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
            <div className="flex items-center justify-between pb-4 border-b border-slate-800">
              <div className="flex items-center space-x-2">
                <span className="text-lg">⚡</span>
                <h2 className="text-lg font-bold text-white">Today&apos;s Daily Mission</h2>
              </div>
              <span className="rounded bg-indigo-950 border border-indigo-700/60 px-2 py-0.5 text-xs font-semibold text-indigo-300">
                {mission?.estimated_minutes || 25} min
              </span>
            </div>

            {mission ? (
              <div className="mt-4 space-y-4">
                <div>
                  <h3 className="text-base font-semibold text-white">{mission.title}</h3>
                  <p className="mt-1 text-sm text-slate-300 leading-relaxed">{mission.description}</p>
                </div>

                {mission.reading_url && (
                  <div className="p-3.5 rounded-lg bg-slate-950 border border-slate-800 text-xs">
                    <span className="text-slate-400">Curriculum reading: </span>
                    <Link
                      href={mission.reading_url}
                      className="text-indigo-400 font-semibold hover:underline ml-1"
                    >
                      Open Concept Study Notes →
                    </Link>
                  </div>
                )}

                {missionDoneMsg && (
                  <div className="p-3 rounded-lg bg-emerald-950/40 border border-emerald-900/60 text-xs text-emerald-300">
                    {missionDoneMsg}
                  </div>
                )}

                <div className="pt-2 flex items-center justify-between">
                  <span className="text-xs text-slate-400">
                    Status:{" "}
                    <span className={`font-semibold ${mission.completed ? "text-emerald-400" : "text-amber-400"}`}>
                      {mission.completed ? "Completed" : "In Progress"}
                    </span>
                  </span>

                  {!mission.completed && (
                    <button
                      onClick={handleCompleteMission}
                      disabled={completingMission}
                      className="rounded-lg bg-indigo-600 px-4 py-2 text-xs font-semibold text-white hover:bg-indigo-500 disabled:opacity-50 transition-all cursor-pointer active:scale-95 disabled:cursor-not-allowed select-none"
                    >
                      {completingMission ? "Updating Twin..." : "Mark Mission Complete"}
                    </button>
                  )}
                </div>
              </div>
            ) : (
              <div className="mt-4 text-center py-6 text-sm text-slate-400">
                <p>No active mission for today yet.</p>
                <Link
                  href="/missions"
                  className="mt-3 inline-block rounded-lg bg-indigo-600 px-4 py-2 text-xs font-semibold text-white hover:bg-indigo-500 transition-all cursor-pointer active:scale-95 select-none"
                >
                  Generate Daily Mission
                </Link>
              </div>
            )}
          </div>

          {/* Quick Concept Mastery Preview */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
            <div className="flex items-center justify-between pb-4 border-b border-slate-800">
              <h2 className="text-lg font-bold text-white">Cognitive Twin Frontier</h2>
              <Link href="/twin" className="text-xs text-indigo-400 hover:underline">
                View all 79 concepts →
              </Link>
            </div>

            <div className="mt-4 divide-y divide-slate-800/80">
              {twin?.mastery_list?.slice(0, 5).map((m) => (
                <div key={m.concept_id} className="py-3 flex items-center justify-between">
                  <div>
                    <span className="text-sm font-semibold text-white">{m.concept_title || m.concept_id}</span>
                    <span className="block text-[11px] text-slate-400 capitalize">
                      Source: {m.source_type.replace("_", " ")}
                    </span>
                  </div>
                  <div className="text-right">
                    <span className="text-sm font-bold text-slate-200">
                      {(m.mastery_score * 100).toFixed(0)}%
                    </span>
                    <span className="block text-[10px] text-slate-500">
                      CI: [{(m.credible_interval_low * 100).toFixed(0)}%-{(m.credible_interval_high * 100).toFixed(0)}%]
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Spaced Retention & Assistant Quick Access */}
        <div className="space-y-6">
          {/* Due Reviews Card */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
            <div className="flex items-center justify-between pb-4 border-b border-slate-800">
              <h2 className="text-base font-bold text-white">Retention Queue</h2>
              <span className="rounded bg-amber-950 border border-amber-800/60 px-2 py-0.5 text-[11px] font-semibold text-amber-300">
                SM-2 Engine
              </span>
            </div>

            <div className="mt-4">
              {dueReviews.length > 0 ? (
                <div className="space-y-3">
                  <p className="text-xs text-slate-300">
                    You have <strong className="text-amber-400">{dueReviews.length} concept(s)</strong> due for spaced
                    retrieval practice today.
                  </p>
                  <Link
                    href="/reviews"
                    className="block w-full text-center rounded-lg bg-amber-600/20 border border-amber-600/40 py-2.5 text-xs font-semibold text-amber-300 hover:bg-amber-600/30 transition-all cursor-pointer active:scale-95 select-none"
                  >
                    Start Revision Session
                  </Link>
                </div>
              ) : (
                <div className="text-center py-4 text-xs text-slate-400">
                  <p>All concepts are within active retention windows.</p>
                  <p className="mt-1 text-emerald-400">No decay scheduled today.</p>
                </div>
              )}
            </div>
          </div>

          {/* AI Teaching Companion Quick Card */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
            <div className="flex items-center space-x-2 pb-4 border-b border-slate-800">
              <span className="text-base">🤖</span>
              <h2 className="text-base font-bold text-white">AI Teaching Companion</h2>
            </div>
            <p className="mt-4 text-xs text-slate-300 leading-relaxed">
              Have a question about mutability, closures, or exceptions? Ask the companion for a grounded explanation
              citing verified genome sources.
            </p>
            <Link
              href="/companion"
              className="mt-4 block w-full text-center rounded-lg bg-indigo-600 py-2.5 text-xs font-semibold text-white hover:bg-indigo-500 transition-all cursor-pointer active:scale-95 select-none"
            >
              Open Companion Chat
            </Link>
          </div>

          {/* Verification Charter Badge */}
          <div className="rounded-2xl border border-slate-800/80 bg-slate-950 p-4 text-[11px] text-slate-500 leading-relaxed">
            <p className="font-semibold text-slate-400 mb-1">🛡️ Deterministic Guarantee</p>
            Scores reflect closed-form Beta distribution mathematics. Evidence is never upgraded without tests, and no
            employment or grade outcomes are guaranteed.
          </div>
        </div>
      </div>
    </div>
  );
}
