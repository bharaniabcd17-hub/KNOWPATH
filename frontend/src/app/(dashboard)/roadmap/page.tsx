"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { RoadmapRead } from "@/types";

export default function RoadmapPage() {
  const [roadmap, setRoadmap] = useState<RoadmapRead | null>(null);
  const [loading, setLoading] = useState(true);
  const [regenerating, setRegenerating] = useState(false);

  const fetchRoadmap = async () => {
    try {
      setLoading(true);
      const data = await api.getRoadmap();
      setRoadmap(data);
    } catch (err) {
      console.error("Roadmap fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRoadmap();
  }, []);

  const handleRegenerate = async () => {
    try {
      setRegenerating(true);
      const updated = await api.regenerateRoadmap();
      setRoadmap(updated);
    } catch (err) {
      console.error("Roadmap regeneration error:", err);
    } finally {
      setRegenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="flex items-center space-x-3 text-slate-400">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent"></div>
          <span className="text-sm">Calculating topological prerequisite roadmap...</span>
        </div>
      </div>
    );
  }

  const items = roadmap?.items || [];

  return (
    <div className="space-y-8 max-w-5xl">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="inline-flex items-center space-x-2 rounded-full bg-indigo-950/80 border border-indigo-700/50 px-3 py-0.5 text-xs font-semibold text-indigo-300 mb-2">
            <span>Goal: {roadmap?.goal_key?.replace("_", " ") || "Python for Placements"}</span>
          </div>
          <h1 className="text-3xl font-extrabold text-white">Adaptive Learning Roadmap</h1>
          <p className="mt-1 text-sm text-slate-400">
            Topologically sorted sequence of missing concepts. Concepts that unblock multiple downstream topics receive
            foundation priority.
          </p>
        </div>

        <div className="w-full sm:w-auto">
          <button
            onClick={handleRegenerate}
            disabled={regenerating}
            className="w-full sm:w-auto rounded-xl border border-slate-700 bg-slate-900 px-4 py-2.5 text-xs font-semibold text-slate-200 hover:text-white hover:bg-slate-800 disabled:opacity-50 transition-all cursor-pointer active:scale-95 select-none flex items-center justify-center space-x-2"
          >
            <span>🔄</span>
            <span>{regenerating ? "Recalculating..." : "Regenerate from Twin"}</span>
          </button>
        </div>
      </div>

      {/* Roadmap List */}
      {items.length > 0 ? (
        <div className="space-y-4">
          {items.map((item, idx) => (
            <div
              key={item.id || item.concept_slug || idx}
              className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:border-slate-700 transition-all"
            >
              <div className="flex items-start space-x-4">
                <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-xl bg-slate-950 border border-slate-800 font-bold text-indigo-400 text-sm">
                  #{item.rank || idx + 1}
                </div>
                <div>
                  <div className="flex items-center space-x-2">
                    <h3 className="text-base font-bold text-white">
                      {item.concept_title || item.concept_slug}
                    </h3>
                    <span className="text-[10px] font-mono text-slate-500">#{item.concept_slug}</span>
                  </div>
                  <p className="mt-1 text-xs text-slate-300 leading-relaxed max-w-xl">
                    {item.reason || "Prerequisite blocker identified in knowledge graph traversal."}
                  </p>
                </div>
              </div>

              <div className="flex sm:flex-col items-center sm:items-end justify-between sm:justify-center gap-2 flex-shrink-0">
                <div className="text-right">
                  <span className="text-xs text-slate-500 block">Current Mastery</span>
                  <span className="text-sm font-bold text-amber-400">
                    {((item.current_mastery || 0) * 100).toFixed(0)}%
                  </span>
                </div>
                <Link
                  href={`/genome/${item.concept_slug}`}
                  className="rounded-lg bg-indigo-600/20 border border-indigo-600/40 px-3.5 py-1.5 text-xs font-semibold text-indigo-300 hover:bg-indigo-600/30 transition-all cursor-pointer active:scale-95 select-none"
                >
                  Study Notes →
                </Link>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-12 text-center">
          <div className="text-4xl mb-3">🎉</div>
          <h2 className="text-xl font-bold text-white">All Goal Concepts Mastered!</h2>
          <p className="mt-2 text-sm text-slate-400 max-w-md mx-auto">
            You have satisfied the target requirements for this track. Switch your goal in Settings or take advanced
            assessments.
          </p>
        </div>
      )}
    </div>
  );
}
