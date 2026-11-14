"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { TwinPageData } from "@/types";

interface CareerTrack {
  id: string;
  title: string;
  description: string;
  requiredConcepts: string[];
}

const CAREER_TRACKS: CareerTrack[] = [
  {
    id: "backend_dev",
    title: "Backend API Engineer (Python)",
    description: "Designing robust web APIs, async database interactions, error handlers, and authentication pipelines.",
    requiredConcepts: [
      "exception_handling",
      "oop_classes",
      "dict_basics",
      "functions_advanced",
      "async_basics",
      "context_managers",
    ],
  },
  {
    id: "data_engineer",
    title: "Data Pipeline & Analytics Engineer",
    description: "Processing structured/unstructured datasets, file streams, generators, and data transformations.",
    requiredConcepts: [
      "generator_functions",
      "list_comprehensions",
      "dict_mutability",
      "files_reading",
      "exception_hierarchy",
      "string_formatting",
    ],
  },
  {
    id: "automation_eng",
    title: "Python Automation & DevOps Specialist",
    description: "Scripting administrative workflows, log parsing, subprocess orchestration, and reliability checks.",
    requiredConcepts: [
      "files_writing",
      "control_flow_loops",
      "exception_handling",
      "string_methods",
      "cli_args",
    ],
  },
];

export default function FuturePathSimulatorPage() {
  const [twin, setTwin] = useState<TwinPageData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const data = await api.getTwin();
        setTwin(data);
      } catch (err) {
        console.error("Twin load error:", err);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="flex items-center space-x-3 text-slate-400">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-purple-500 border-t-transparent"></div>
          <span className="text-sm">Simulating capability readiness across career paths...</span>
        </div>
      </div>
    );
  }

  const masteryMap = new Map<string, number>();
  twin?.mastery_list?.forEach((m) => {
    masteryMap.set(m.concept_id, m.mastery_score);
  });

  return (
    <div className="space-y-8 max-w-5xl">
      {/* Header */}
      <div className="border-b border-slate-800 pb-6">
        <div className="inline-flex items-center space-x-2 rounded-full bg-purple-950/80 border border-purple-700/50 px-3 py-0.5 text-xs font-semibold text-purple-300 mb-2">
          <span>Prerequisite Pathway Projection</span>
        </div>
        <h1 className="text-3xl font-extrabold text-white">FuturePath Simulator</h1>
        <p className="mt-1 text-sm text-slate-400">
          Simulate your capability alignment with specific technical software roles based on demonstrated Knowledge
          Genome concept mastery.
        </p>
      </div>

      {/* Tracks Grid */}
      <div className="space-y-6">
        {CAREER_TRACKS.map((track) => {
          let masteredInTrack = 0;
          const missing: string[] = [];

          track.requiredConcepts.forEach((c) => {
            const score = masteryMap.get(c) || 0.1;
            if (score >= 0.7) {
              masteredInTrack++;
            } else {
              missing.push(c);
            }
          });

          const readinessPct = Math.round((masteredInTrack / track.requiredConcepts.length) * 100);

          return (
            <div
              key={track.id}
              className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 sm:p-8 space-y-5"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <h2 className="text-xl font-bold text-white">{track.title}</h2>
                  <p className="mt-1 text-xs text-slate-400 max-w-xl">{track.description}</p>
                </div>
                <div className="text-right sm:flex-shrink-0">
                  <span className="text-2xl font-extrabold text-purple-400">{readinessPct}%</span>
                  <span className="block text-[10px] text-slate-500 uppercase tracking-wider font-semibold">
                    Capability Readiness
                  </span>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="w-full bg-slate-950 rounded-full h-2.5 overflow-hidden border border-slate-800">
                <div
                  className="bg-gradient-to-r from-purple-500 to-indigo-500 h-full rounded-full transition-all duration-500"
                  style={{ width: `${readinessPct}%` }}
                ></div>
              </div>

              {/* Missing Foundations Breakdown */}
              <div className="pt-2">
                <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider block mb-2">
                  Prerequisite Breakdown
                </span>
                {missing.length > 0 ? (
                  <div className="flex flex-wrap gap-2">
                    {missing.map((m) => (
                      <Link
                        key={m}
                        href={`/genome/${m}`}
                        className="px-2.5 py-1 rounded-lg bg-rose-950/40 border border-rose-900/60 text-xs text-rose-300 hover:bg-rose-900/50 transition-colors"
                      >
                        ⚠️ Missing: #{m}
                      </Link>
                    ))}
                  </div>
                ) : (
                  <div className="text-xs text-emerald-400 font-medium">
                    ✓ All core prerequisite concepts satisfied for this specialization!
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Compliance Disclaimer */}
      <div className="p-4 rounded-xl border border-slate-800 bg-slate-950 text-xs text-slate-500 leading-relaxed">
        <strong>Important Notice:</strong> FuturePath Simulator projects prerequisite readiness based strictly on
        demonstrated cognitive mastery. KNOWPATH does not guarantee employment, interviews, or salaries.
      </div>
    </div>
  );
}
