"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { ReviewItem } from "@/types";

export default function ReviewsPage() {
  const [reviews, setReviews] = useState<ReviewItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionMsg, setActionMsg] = useState<string | null>(null);

  const fetchDue = async () => {
    try {
      setLoading(true);
      const data = await api.getDueReviews();
      setReviews(data);
    } catch (err) {
      console.error("Reviews fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDue();
  }, []);

  const handleReviewAction = async (conceptSlug: string, result: "pass" | "fail") => {
    try {
      await api.completeReview(conceptSlug, result);
      setActionMsg(
        result === "pass"
          ? `✓ Passed! Spaced retention interval expanded for ${conceptSlug}.`
          : `✗ Failed. Retention interval reset to 1 day for ${conceptSlug}.`
      );
      fetchDue();
    } catch (err: any) {
      setActionMsg(`Failed: ${err?.message || "Error"}`);
    }
  };

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="flex items-center space-x-3 text-slate-400">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-amber-500 border-t-transparent"></div>
          <span className="text-sm">Calculating SM-2 retention decay curves...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-4xl">
      {/* Header */}
      <div className="border-b border-slate-800 pb-6">
        <div className="inline-flex items-center space-x-2 rounded-full bg-amber-950/80 border border-amber-700/50 px-3 py-0.5 text-xs font-semibold text-amber-300 mb-2">
          <span>SM-2 Memory Retention Algorithm</span>
        </div>
        <h1 className="text-3xl font-extrabold text-white">Spaced Retrieval Reviews</h1>
        <p className="mt-1 text-sm text-slate-400">
          Knowledge naturally decays over time. Conduct quick active recall checks to prevent recency decay penalties
          on your Cognitive Twin.
        </p>
      </div>

      {actionMsg && (
        <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-200">
          {actionMsg}
        </div>
      )}

      {reviews.length > 0 ? (
        <div className="space-y-4">
          {reviews.map((rev) => (
            <div
              key={rev.id || rev.concept_slug}
              className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4"
            >
              <div>
                <div className="flex items-center space-x-2">
                  <span className="text-lg">🔄</span>
                  <h3 className="text-base font-bold text-white">{rev.concept_title || rev.concept_slug}</h3>
                  <span className="text-xs text-slate-500 font-mono">#{rev.concept_slug}</span>
                </div>
                <div className="mt-2 flex items-center space-x-4 text-xs text-slate-400">
                  <span>Current Interval: <strong className="text-white">{rev.interval_days} days</strong></span>
                  <span>Ease Factor: <strong className="text-amber-400">{rev.ease_factor.toFixed(2)}</strong></span>
                  <span>Due: <strong className="text-rose-400">Today</strong></span>
                </div>
              </div>

              <div className="flex flex-wrap items-center gap-2 sm:gap-3">
                <Link
                  href={`/genome/${rev.concept_slug}`}
                  className="rounded-lg border border-slate-800 bg-slate-950 px-3 py-2 text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-900 transition-all cursor-pointer active:scale-95 select-none"
                >
                  Review Notes
                </Link>

                <button
                  onClick={() => handleReviewAction(rev.concept_slug, "fail")}
                  className="rounded-lg border border-rose-900/60 bg-rose-950/40 px-3 py-2 text-xs font-semibold text-rose-300 hover:bg-rose-950/70 transition-all cursor-pointer active:scale-95 select-none"
                >
                  Forgot (Reset)
                </button>

                <button
                  onClick={() => handleReviewAction(rev.concept_slug, "pass")}
                  className="rounded-lg bg-emerald-600 px-3.5 py-2 text-xs font-semibold text-white hover:bg-emerald-500 transition-all cursor-pointer active:scale-95 select-none"
                >
                  Remembered (+Days)
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-12 text-center">
          <div className="text-4xl mb-3">🌿</div>
          <h2 className="text-xl font-bold text-white">All Concept Memories Intact</h2>
          <p className="mt-2 text-sm text-slate-400 max-w-md mx-auto">
            You have no reviews due today! All verified concepts are currently within their optimal retention windows.
          </p>
        </div>
      )}
    </div>
  );
}
