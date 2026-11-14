"use client";

import React, { useState } from "react";
import Link from "next/link";

interface PracticalProject {
  id: string;
  title: string;
  difficulty: "beginner" | "intermediate" | "advanced";
  estimatedHours: number;
  description: string;
  concepts: string[];
  prerequisitesMet: boolean;
}

const PRACTICAL_PROJECTS: PracticalProject[] = [
  {
    id: "proj_cli_dedup",
    title: "CLI File Content Deduplicator",
    difficulty: "beginner",
    estimatedHours: 2,
    description:
      "Construct a command-line script that scans a directory, calculates file hashes, and identifies duplicate contents using dicts and file I/O streams.",
    concepts: ["files_reading", "dict_basics", "hash_intro", "cli_args"],
    prerequisitesMet: true,
  },
  {
    id: "proj_lru_cache",
    title: "Custom LRU Cache Decorator",
    difficulty: "intermediate",
    estimatedHours: 3,
    description:
      "Implement a function decorator from scratch that caches up to N return values, evicting the least recently used item when capacity is exceeded.",
    concepts: ["decorators_intro", "closures_basics", "dict_mutability", "doubly_linked_concepts"],
    prerequisitesMet: true,
  },
  {
    id: "proj_log_parser",
    title: "Resilient Log Stream Parser",
    difficulty: "intermediate",
    estimatedHours: 2.5,
    description:
      "Build a streaming generator that processes gigabyte-scale server log lines, handling malformed lines with custom exception hierarchies.",
    concepts: ["generator_functions", "exception_hierarchy", "string_parsing", "context_managers"],
    prerequisitesMet: false,
  },
  {
    id: "proj_async_crawler",
    title: "Concurrent Task Queue Worker",
    difficulty: "advanced",
    estimatedHours: 5,
    description:
      "Design an asynchronous in-memory job queue with worker tasks, retry backoff logic, and graceful shutdown signal handling.",
    concepts: ["async_basics", "exception_handling", "queue_data_structures", "oop_classes"],
    prerequisitesMet: false,
  },
];

export default function ProjectsPage() {
  const [selectedFilter, setSelectedFilter] = useState<string>("all");

  const filtered = PRACTICAL_PROJECTS.filter((p) => {
    if (selectedFilter === "all") return true;
    return p.difficulty === selectedFilter;
  });

  return (
    <div className="space-y-8 max-w-5xl">
      {/* Header */}
      <div className="border-b border-slate-800 pb-6">
        <div className="inline-flex items-center space-x-2 rounded-full bg-teal-950/80 border border-teal-700/50 px-3 py-0.5 text-xs font-semibold text-teal-300 mb-2">
          <span>Hands-On Capability Synthesis</span>
        </div>
        <h1 className="text-3xl font-extrabold text-white">Practical Challenges & Projects</h1>
        <p className="mt-1 text-sm text-slate-400">
          Reinforce acquired concepts with real-world technical projects. Each project specifies exact prerequisite
          concepts from the Knowledge Genome.
        </p>
      </div>

      {/* Filter Tabs */}
      <div className="flex flex-wrap gap-2">
        {["all", "beginner", "intermediate", "advanced"].map((d) => (
          <button
            key={d}
            onClick={() => setSelectedFilter(d)}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold capitalize transition-all cursor-pointer active:scale-95 select-none ${
              selectedFilter === d
                ? "bg-teal-600 text-white shadow-md shadow-teal-600/20"
                : "bg-slate-900 text-slate-400 hover:text-white hover:bg-slate-800"
            }`}
          >
            {d}
          </button>
        ))}
      </div>

      {/* Projects Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {filtered.map((proj) => (
          <div
            key={proj.id}
            className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 flex flex-col justify-between hover:border-slate-700 transition-all"
          >
            <div>
              <div className="flex items-center justify-between mb-3">
                <span
                  className={`px-2 py-0.5 rounded text-[10px] font-semibold uppercase ${
                    proj.difficulty === "beginner"
                      ? "bg-emerald-950 text-emerald-300 border border-emerald-800/50"
                      : proj.difficulty === "intermediate"
                      ? "bg-amber-950 text-amber-300 border border-amber-800/50"
                      : "bg-purple-950 text-purple-300 border border-purple-800/50"
                  }`}
                >
                  {proj.difficulty}
                </span>
                <span className="text-xs text-slate-400">⏱️ ~{proj.estimatedHours} hrs</span>
              </div>

              <h3 className="text-base font-bold text-white">{proj.title}</h3>
              <p className="mt-2 text-xs text-slate-300 leading-relaxed">{proj.description}</p>

              {/* Concept tags */}
              <div className="mt-4 pt-3 border-t border-slate-800/80">
                <span className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider block mb-2">
                  Mapped Genome Concepts
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {proj.concepts.map((c) => (
                    <Link
                      key={c}
                      href={`/genome/${c}`}
                      className="px-2 py-0.5 rounded bg-slate-950 border border-slate-800 text-[10px] font-mono text-teal-400 hover:border-teal-500 transition-colors"
                    >
                      #{c}
                    </Link>
                  ))}
                </div>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-800/80 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <span
                className={`text-xs font-semibold ${
                  proj.prerequisitesMet ? "text-emerald-400" : "text-amber-400"
                }`}
              >
                {proj.prerequisitesMet ? "✓ Prerequisites Satisfied" : "⚠️ Prerequisite Gaps"}
              </span>

              <Link
                href="/companion"
                className="w-full sm:w-auto text-center rounded-lg bg-teal-600 px-4 py-2 text-xs font-semibold text-white hover:bg-teal-500 transition-all cursor-pointer active:scale-95 select-none"
              >
                Discuss with Tutor →
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
