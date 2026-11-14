"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { ConceptSummary, GenomeGraph } from "@/types";

export default function KnowledgeGenomePage() {
  const [concepts, setConcepts] = useState<ConceptSummary[]>([]);
  const [graph, setGraph] = useState<GenomeGraph | null>(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>("all");
  const [viewMode, setViewMode] = useState<"grid" | "dag">("grid");

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const [cList, gData] = await Promise.allSettled([
          api.getGenomeConcepts(),
          api.getGenomeGraph(),
        ]);
        if (cList.status === "fulfilled") setConcepts(cList.value);
        if (gData.status === "fulfilled") setGraph(gData.value);
      } catch (err) {
        console.error("Genome loading error:", err);
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
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent"></div>
          <span className="text-sm">Mapping Knowledge Genome DAG (79 concepts, 118 edges)...</span>
        </div>
      </div>
    );
  }

  const filtered = concepts.filter((c) => {
    const matchesSearch =
      c.title.toLowerCase().includes(search.toLowerCase()) ||
      c.slug.toLowerCase().includes(search.toLowerCase()) ||
      c.description.toLowerCase().includes(search.toLowerCase());

    if (!matchesSearch) return false;
    if (selectedDifficulty !== "all" && String(c.difficulty) !== selectedDifficulty) return false;
    return true;
  });

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="inline-flex items-center space-x-2 rounded-full bg-teal-950/80 border border-teal-700/50 px-3 py-0.5 text-xs font-semibold text-teal-300 mb-2">
            <span>Cycle-Free DAG Architecture</span>
          </div>
          <h1 className="text-3xl font-extrabold text-white">Knowledge Genome</h1>
          <p className="mt-1 text-sm text-slate-400">
            Explore 79 verified Python concepts connected by 118 prerequisite edges.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => setViewMode("grid")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              viewMode === "grid" ? "bg-indigo-600 text-white" : "bg-slate-900 text-slate-400 hover:text-white"
            }`}
          >
            Grid Explorer
          </button>
          <button
            onClick={() => setViewMode("dag")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              viewMode === "dag" ? "bg-teal-600 text-white" : "bg-slate-900 text-slate-400 hover:text-white"
            }`}
          >
            Prerequisite Graph
          </button>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="w-full sm:w-80">
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search genome concepts..."
            className="w-full rounded-lg border border-slate-700 bg-slate-900 px-3.5 py-2 text-xs text-white placeholder-slate-500 focus:border-teal-500 focus:outline-none"
          />
        </div>

        <div className="flex space-x-2 w-full sm:w-auto">
          {["all", "beginner", "intermediate", "advanced"].map((d) => (
            <button
              key={d}
              onClick={() => setSelectedDifficulty(d)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium capitalize transition-colors ${
                selectedDifficulty === d
                  ? "bg-teal-600 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {d}
            </button>
          ))}
        </div>
      </div>

      {/* DAG Visualization View */}
      {viewMode === "dag" && graph && (
        <div className="rounded-2xl border border-slate-800 bg-slate-950 p-6">
          <div className="flex items-center justify-between pb-4 border-b border-slate-800">
            <h2 className="text-base font-bold text-white">Topological Prerequisite DAG</h2>
            <span className="text-xs text-teal-400 font-mono">
              Nodes: {graph.nodes.length} | Edges: {graph.edges.length}
            </span>
          </div>

          <div className="mt-4 p-4 rounded-xl bg-slate-900/60 border border-slate-800/80 max-h-[500px] overflow-y-auto">
            <p className="text-xs text-slate-400 mb-4">
              Click any node in the prerequisite structure to open its dedicated curriculum notes and linked assessment items.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
              {graph.nodes.slice(0, 30).map((node) => (
                <Link
                  key={node.id}
                  href={`/genome/${node.id}`}
                  className="p-3 rounded-lg border border-slate-800 bg-slate-950 hover:border-teal-500 hover:bg-slate-900 transition-all flex flex-col justify-between"
                >
                  <div>
                    <span className="text-xs font-bold text-white">{node.label || node.title || node.id}</span>
                    <span className="block text-[10px] text-slate-500 font-mono mt-0.5">{node.id}</span>
                  </div>
                  <div className="mt-2 flex items-center justify-between text-[10px]">
                    <span className="capitalize px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">
                      {node.difficulty}
                    </span>
                    <span className="text-teal-400 font-semibold">Inspect →</span>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Grid Explorer View */}
      {viewMode === "grid" && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {filtered.map((concept) => (
            <Link
              key={concept.slug}
              href={`/genome/${concept.slug}`}
              className="group rounded-2xl border border-slate-800 bg-slate-900/60 p-5 hover:border-teal-500/50 hover:bg-slate-900 transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-semibold uppercase ${
                      String(concept.difficulty) === "beginner"
                        ? "bg-emerald-950 text-emerald-300 border border-emerald-800/50"
                        : String(concept.difficulty) === "intermediate"
                        ? "bg-amber-950 text-amber-300 border border-amber-800/50"
                        : "bg-purple-950 text-purple-300 border border-purple-800/50"
                    }`}
                  >
                    {concept.difficulty}
                  </span>
                  <span className="text-xs text-slate-500 font-mono">#{concept.slug}</span>
                </div>

                <h3 className="text-base font-bold text-white group-hover:text-teal-300 transition-colors">
                  {concept.title}
                </h3>
                <p className="mt-2 text-xs text-slate-400 line-clamp-3 leading-relaxed">
                  {concept.description}
                </p>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
                <span className="text-slate-500">Prereqs / Dependents mapped</span>
                <span className="text-teal-400 font-semibold group-hover:translate-x-1 transition-transform">
                  Study Notes →
                </span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
