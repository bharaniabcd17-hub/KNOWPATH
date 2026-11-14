"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuthStore } from "@/stores/auth";

interface NavItem {
  name: string;
  href: string;
  icon: string;
  badge?: string;
  adminOnly?: boolean;
}

const NAV_ITEMS: NavItem[] = [
  { name: "Overview", href: "/dashboard", icon: "📊" },
  { name: "Cognitive Twin", href: "/twin", icon: "🧠", badge: "Live" },
  { name: "Knowledge Genome", href: "/genome", icon: "🧬" },
  { name: "Diagnostic & Tests", href: "/assessment", icon: "🎯" },
  { name: "Adaptive Roadmap", href: "/roadmap", icon: "🗺️" },
  { name: "Daily Missions", href: "/missions", icon: "⚡" },
  { name: "AI Companion", href: "/companion", icon: "🤖" },
  { name: "Spaced Reviews", href: "/reviews", icon: "🔄" },
  { name: "Practical Projects", href: "/projects", icon: "💻" },
  { name: "Capability Portfolio", href: "/portfolio", icon: "📜" },
  { name: "FuturePath Simulator", href: "/futurepath", icon: "🔮" },
  { name: "Disputes & Integrity", href: "/disputes", icon: "⚖️" },
  { name: "Settings & Privacy", href: "/settings", icon: "⚙️" },
  { name: "Admin Portal", href: "/admin", icon: "🛡️", adminOnly: true },
];

interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
}

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  const pathname = usePathname();
  const { user } = useAuthStore();

  const isAdmin = user?.role === "admin";

  const content = (
    <div className="flex flex-col justify-between h-full bg-slate-950">
      <div>
        {/* Brand header */}
        <div className="flex h-16 items-center justify-between px-6 border-b border-slate-800">
          <Link
            href="/dashboard"
            onClick={onClose}
            className="flex items-center space-x-2.5 group cursor-pointer"
          >
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white p-0.5 shadow-md shadow-indigo-500/20 group-hover:scale-105 transition-transform overflow-hidden border border-indigo-400/40 flex-shrink-0">
              <img src="/images/knowpath-logo.jpg" alt="KnowPath Logo" className="h-full w-full object-contain" />
            </div>
            <div>
              <span className="font-bold text-white tracking-tight">KNOWPATH</span>
              <span className="block text-[10px] font-medium text-indigo-400 -mt-1">Learner Intelligence</span>
            </div>
          </Link>

          {/* Close button for mobile drawer */}
          {onClose && (
            <button
              onClick={onClose}
              className="lg:hidden p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-900 transition-colors cursor-pointer active:scale-95"
              aria-label="Close sidebar"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>

        {/* Navigation list */}
        <div className="px-3 py-4 overflow-y-auto max-h-[calc(100vh-140px)]">
          <div className="px-3 pb-2 text-[10px] font-bold uppercase tracking-wider text-slate-500">
            Intelligence Platform
          </div>
          <nav className="space-y-1">
            {NAV_ITEMS.map((item) => {
              if (item.adminOnly && !isAdmin) return null;
              const isActive = pathname === item.href || pathname.startsWith(item.href + "/");

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={onClose}
                  className={`group flex items-center justify-between px-3 py-2.5 text-sm font-medium rounded-lg transition-all cursor-pointer active:scale-98 ${
                    isActive
                      ? "bg-indigo-600/20 text-indigo-300 border border-indigo-500/40 font-semibold shadow-sm"
                      : "text-slate-400 hover:bg-slate-900 hover:text-slate-100"
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <span className="text-base group-hover:scale-110 transition-transform">{item.icon}</span>
                    <span>{item.name}</span>
                  </div>
                  {item.badge && (
                    <span className="rounded bg-indigo-500/20 px-1.5 py-0.5 text-[10px] font-semibold text-indigo-300">
                      {item.badge}
                    </span>
                  )}
                </Link>
              );
            })}
          </nav>
        </div>
      </div>

      {/* User profile footer */}
      <div className="p-3 border-t border-slate-800">
        <Link
          href="/settings"
          onClick={onClose}
          className="flex items-center space-x-3 px-3 py-2 rounded-xl bg-slate-900/60 border border-slate-800/80 hover:border-indigo-500/40 hover:bg-slate-900 transition-all cursor-pointer group"
        >
          <div className="relative flex h-9 w-9 items-center justify-center rounded-full bg-white p-0.5 border border-indigo-500/50 overflow-hidden shadow-sm flex-shrink-0 group-hover:scale-105 transition-transform">
            <img
              src="/images/knowpath-avatar.jpg"
              alt="Learner Profile Picture"
              className="h-full w-full rounded-full object-cover"
            />
            <span className="absolute bottom-0 right-0 h-2 w-2 rounded-full bg-emerald-500 ring-1 ring-slate-950" title="Active learner"></span>
          </div>
          <div className="overflow-hidden flex-1">
            <p className="text-xs font-semibold text-slate-200 truncate group-hover:text-white transition-colors">
              {user?.email || "Learner"}
            </p>
            <p className="text-[10px] text-indigo-400 capitalize flex items-center">
              <span>{user?.role || "learner"} account</span>
            </p>
          </div>
        </Link>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Sticky Sidebar */}
      <aside className="hidden lg:flex w-64 flex-shrink-0 border-r border-slate-800 bg-slate-950 flex-col justify-between h-screen sticky top-0 z-30">
        {content}
      </aside>

      {/* Mobile / Tablet Off-canvas Drawer */}
      {isOpen && (
        <div className="fixed inset-0 z-50 lg:hidden flex">
          {/* Backdrop overlay */}
          <div
            className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm transition-opacity cursor-pointer"
            onClick={onClose}
            aria-hidden="true"
          />

          {/* Drawer content */}
          <div className="relative flex-1 flex flex-col max-w-xs w-full bg-slate-950 border-r border-slate-800 shadow-2xl z-10 animate-in slide-in-from-left duration-200">
            {content}
          </div>
        </div>
      )}
    </>
  );
}
