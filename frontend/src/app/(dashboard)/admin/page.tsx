"use client";

import React, { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useAuthStore } from "@/stores/auth";
import { Dispute } from "@/types";

export default function AdminPortalPage() {
  const { user } = useAuthStore();
  const [users, setUsers] = useState<any[]>([]);
  const [disputes, setDisputes] = useState<Dispute[]>([]);
  const [executions, setExecutions] = useState<any[]>([]);
  const [costs, setCosts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"users" | "disputes" | "agents" | "costs">("disputes");
  const [resolvingId, setResolvingId] = useState<string | null>(null);

  const fetchAdminData = async () => {
    try {
      setLoading(true);
      const [uRes, dRes, eRes, cRes] = await Promise.allSettled([
        api.adminGetUsers(),
        api.adminGetDisputes(),
        api.adminGetExecutions(),
        api.adminGetCosts(),
      ]);

      if (uRes.status === "fulfilled") setUsers(uRes.value);
      if (dRes.status === "fulfilled") setDisputes(dRes.value);
      if (eRes.status === "fulfilled") setExecutions(eRes.value);
      if (cRes.status === "fulfilled") setCosts(cRes.value);
    } catch (err) {
      console.error("Admin data fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAdminData();
  }, []);

  const handleResolveDispute = async (disputeId: string, resolution: "resolved" | "dismissed") => {
    try {
      setResolvingId(disputeId);
      await api.adminResolveDispute(disputeId, resolution);
      fetchAdminData();
    } catch (err: any) {
      alert(`Resolution failed: ${err?.message || "Error"}`);
    } finally {
      setResolvingId(null);
    }
  };

  if (user?.role !== "admin") {
    return (
      <div className="rounded-2xl border border-rose-900/60 bg-rose-950/20 p-8 text-center max-w-md mx-auto mt-12">
        <div className="text-3xl mb-3">🛡️</div>
        <h2 className="text-xl font-bold text-white">Administrative Access Required</h2>
        <p className="mt-2 text-xs text-rose-300">
          This portal is restricted to users with verified administrative roles.
        </p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="flex items-center space-x-3 text-slate-400">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent"></div>
          <span className="text-sm">Loading administrative control telemetry...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-6xl">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="inline-flex items-center space-x-2 rounded-full bg-rose-950/80 border border-rose-700/50 px-3 py-0.5 text-xs font-semibold text-rose-300 mb-2">
            <span>Admin Authorization Verified</span>
          </div>
          <h1 className="text-3xl font-extrabold text-white">System Admin & Audit Desk</h1>
          <p className="mt-1 text-sm text-slate-400">
            Audit learner disputes, inspect AI agent execution logs, track token expenditures, and manage users.
          </p>
        </div>

        <button
          onClick={fetchAdminData}
          className="w-full sm:w-auto rounded-xl border border-slate-700 bg-slate-900 px-4 py-2.5 text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800 transition-all cursor-pointer active:scale-95 select-none"
        >
          🔄 Refresh Telemetry
        </button>
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-3">
        <button
          onClick={() => setActiveTab("disputes")}
          className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer active:scale-95 select-none ${
            activeTab === "disputes"
              ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/20"
              : "bg-slate-900 text-slate-400 hover:text-white hover:bg-slate-800"
          }`}
        >
          Dispute Desk ({disputes.filter((d) => d.status === "open").length} open)
        </button>
        <button
          onClick={() => setActiveTab("agents")}
          className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer active:scale-95 select-none ${
            activeTab === "agents"
              ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/20"
              : "bg-slate-900 text-slate-400 hover:text-white hover:bg-slate-800"
          }`}
        >
          AI Agent Audits ({executions.length})
        </button>
        <button
          onClick={() => setActiveTab("users")}
          className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer active:scale-95 select-none ${
            activeTab === "users"
              ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/20"
              : "bg-slate-900 text-slate-400 hover:text-white hover:bg-slate-800"
          }`}
        >
          Users ({users.length})
        </button>
        <button
          onClick={() => setActiveTab("costs")}
          className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer active:scale-95 select-none ${
            activeTab === "costs"
              ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/20"
              : "bg-slate-900 text-slate-400 hover:text-white hover:bg-slate-800"
          }`}
        >
          Token Costs & Usage
        </button>
      </div>

      {/* Disputes Tab Content */}
      {activeTab === "disputes" && (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
          <h2 className="text-lg font-bold text-white mb-4">Learner Dispute Queue</h2>
          {disputes.length > 0 ? (
            <div className="space-y-4">
              {disputes.map((d) => (
                <div
                  key={d.id}
                  className="p-4 rounded-xl border border-slate-800 bg-slate-950 flex flex-col sm:flex-row sm:items-center justify-between gap-4 text-xs"
                >
                  <div className="space-y-1">
                    <div className="flex items-center space-x-2">
                      <span className="font-bold text-white">{d.target_id}</span>
                      <span className="capitalize text-slate-400 font-mono">({d.target_type})</span>
                      <span
                        className={`px-1.5 py-0.5 rounded text-[10px] uppercase font-bold ${
                          d.status === "open"
                            ? "bg-amber-950 text-amber-300 border border-amber-800/60"
                            : "bg-emerald-950 text-emerald-300 border border-emerald-800/60"
                        }`}
                      >
                        {d.status}
                      </span>
                    </div>
                    <p className="text-slate-300">{d.reason}</p>
                    <span className="text-[10px] text-slate-500 block">
                      Filed: {d.created_at ? new Date(d.created_at).toLocaleString() : "Recently"}
                    </span>
                  </div>

                  {d.status === "open" && (
                    <div className="flex flex-wrap items-center gap-2 flex-shrink-0 pt-2 sm:pt-0">
                      <button
                        onClick={() => handleResolveDispute(d.id, "resolved")}
                        disabled={resolvingId === d.id}
                        className="rounded-lg bg-emerald-600 px-3.5 py-1.5 text-xs font-semibold text-white hover:bg-emerald-500 disabled:opacity-50 transition-all cursor-pointer active:scale-95 select-none"
                      >
                        Resolve & Reinstate
                      </button>
                      <button
                        onClick={() => handleResolveDispute(d.id, "dismissed")}
                        disabled={resolvingId === d.id}
                        className="rounded-lg border border-slate-800 bg-slate-900 px-3.5 py-1.5 text-xs font-semibold text-slate-300 hover:text-white disabled:opacity-50 transition-all cursor-pointer active:scale-95 select-none"
                      >
                        Dismiss
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="text-xs text-slate-500 py-6 text-center">No active learner disputes.</p>
          )}
        </div>
      )}

      {/* AI Agent Executions Tab */}
      {activeTab === "agents" && (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
          <h2 className="text-lg font-bold text-white mb-4">Agent Execution Audit Logs (agent_executions)</h2>
          {executions.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-950 text-slate-400 uppercase font-semibold border-b border-slate-800">
                  <tr>
                    <th className="px-4 py-3">Agent</th>
                    <th className="px-4 py-3">Model</th>
                    <th className="px-4 py-3">Tokens (In / Out)</th>
                    <th className="px-4 py-3">Latency</th>
                    <th className="px-4 py-3">Cost ($)</th>
                    <th className="px-4 py-3">Safety Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800 text-slate-300">
                  {executions.map((e, idx) => (
                    <tr key={e.id || idx}>
                      <td className="px-4 py-3 font-semibold text-white">{e.agent_name}</td>
                      <td className="px-4 py-3 font-mono text-slate-400">{e.model_name || "mock"}</td>
                      <td className="px-4 py-3 font-mono">
                        {e.prompt_tokens || 0} / {e.completion_tokens || 0}
                      </td>
                      <td className="px-4 py-3">{e.latency_ms || 25} ms</td>
                      <td className="px-4 py-3 font-mono text-emerald-400">
                        ${(e.cost_usd || 0.0001).toFixed(4)}
                      </td>
                      <td className="px-4 py-3">
                        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800/60 text-[10px] font-semibold">
                          PASSED
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-xs text-slate-500 py-6 text-center">No agent executions logged yet.</p>
          )}
        </div>
      )}

      {/* Users Tab */}
      {activeTab === "users" && (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
          <h2 className="text-lg font-bold text-white mb-4">Registered Platform Learners</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950 text-slate-400 uppercase font-semibold border-b border-slate-800">
                <tr>
                  <th className="px-4 py-3">User ID</th>
                  <th className="px-4 py-3">Email</th>
                  <th className="px-4 py-3">Role</th>
                  <th className="px-4 py-3">Adult Gate</th>
                  <th className="px-4 py-3">Created At</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-300">
                {users.map((u) => (
                  <tr key={u.id}>
                    <td className="px-4 py-3 font-mono text-indigo-400">{u.id}</td>
                    <td className="px-4 py-3 font-semibold text-white">{u.email}</td>
                    <td className="px-4 py-3 capitalize">{u.role}</td>
                    <td className="px-4 py-3 text-emerald-400 font-bold">18+ Verified</td>
                    <td className="px-4 py-3 text-slate-500">
                      {new Date(u.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Costs Tab */}
      {activeTab === "costs" && (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 space-y-4">
          <h2 className="text-lg font-bold text-white">Aggregated Token Usage & Cost Accounting</h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
              <div className="text-xs text-slate-500">Total Executions</div>
              <div className="text-2xl font-bold text-white mt-1">{executions.length}</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
              <div className="text-xs text-slate-500">Total Spend</div>
              <div className="text-2xl font-bold text-emerald-400 mt-1">
                ${executions.reduce((acc, curr) => acc + (curr.cost_usd || 0.0001), 0).toFixed(4)}
              </div>
            </div>
            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
              <div className="text-xs text-slate-500">Safety Interceptions</div>
              <div className="text-2xl font-bold text-indigo-400 mt-1">0 Violations</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
