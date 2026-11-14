"use client";

import React from "react";
import Link from "next/link";

interface NotificationItem {
  id: string;
  type: "review" | "diagnostic" | "dispute" | "milestone";
  title: string;
  description: string;
  time: string;
  actionUrl?: string;
}

const SAMPLE_NOTIFICATIONS: NotificationItem[] = [
  {
    id: "notif_1",
    type: "review",
    title: "Spaced Retention Check Due",
    description: "Your mastery estimate for list_mutability is approaching its 60-day recency interval. Take a 2-min review.",
    time: "Today",
    actionUrl: "/reviews",
  },
  {
    id: "notif_2",
    type: "milestone",
    title: "Cognitive Twin Calibrated",
    description: "Diagnostic session successfully established baseline credible intervals across 15 core concepts.",
    time: "Yesterday",
    actionUrl: "/twin",
  },
  {
    id: "notif_3",
    type: "diagnostic",
    title: "New Daily Mission Ready",
    description: "Today's high-leverage micro-mission for Python for Placements is ready to study.",
    time: "2 days ago",
    actionUrl: "/missions",
  },
];

export default function NotificationsPage() {
  return (
    <div className="space-y-8 max-w-4xl">
      {/* Header */}
      <div className="border-b border-slate-800 pb-6">
        <h1 className="text-3xl font-extrabold text-white">Notifications & Alerts</h1>
        <p className="mt-1 text-sm text-slate-400">
          Timely alerts regarding spaced retrieval schedules, dispute updates, and learning milestones.
        </p>
      </div>

      <div className="space-y-4">
        {SAMPLE_NOTIFICATIONS.map((n) => (
          <div
            key={n.id}
            className="p-5 rounded-2xl border border-slate-800 bg-slate-900/60 flex flex-col sm:flex-row sm:items-center justify-between gap-4"
          >
            <div className="flex items-start space-x-3.5">
              <span className="text-xl">
                {n.type === "review"
                  ? "🔄"
                  : n.type === "milestone"
                  ? "🏆"
                  : n.type === "dispute"
                  ? "⚖️"
                  : "⚡"}
              </span>
              <div>
                <h3 className="text-sm font-bold text-white">{n.title}</h3>
                <p className="mt-1 text-xs text-slate-300 leading-relaxed max-w-xl">{n.description}</p>
                <span className="text-[10px] text-slate-500 mt-1 block">{n.time}</span>
              </div>
            </div>

            {n.actionUrl && (
              <Link
                href={n.actionUrl}
                className="rounded-lg bg-indigo-600/20 border border-indigo-600/40 px-3.5 py-1.5 text-xs font-semibold text-indigo-300 hover:bg-indigo-600/30 transition-colors text-center"
              >
                View →
              </Link>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
