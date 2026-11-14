"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/stores/auth";

interface HeaderProps {
  onMenuClick?: () => void;
}

export default function Header({ onMenuClick }: HeaderProps) {
  const router = useRouter();
  const { user, logout } = useAuthStore();
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const handleSignOut = async () => {
    await logout();
    router.push("/login");
  };

  return (
    <header className="sticky top-0 z-40 flex h-16 w-full items-center justify-between border-b border-slate-800 bg-slate-950/80 px-4 sm:px-6 backdrop-blur-md">
      <div className="flex items-center space-x-3 sm:space-x-4">
        {/* Mobile Hamburger Menu Toggle */}
        <button
          onClick={onMenuClick}
          className="lg:hidden p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-900 transition-colors cursor-pointer active:scale-95"
          aria-label="Open navigation menu"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        <div className="flex items-center space-x-2 text-xs text-slate-400">
          <span className="font-semibold text-slate-200 hidden sm:inline">Domain</span>
          <span className="hidden sm:inline">/</span>
          <span className="text-indigo-400 font-medium truncate max-w-[180px] sm:max-w-none">
            Python Programming Fundamentals
          </span>
        </div>
      </div>

      <div className="flex items-center space-x-2 sm:space-x-4">
        {/* Quick Diagnostic Pill */}
        <Link
          href="/assessment/diagnostic"
          className="hidden sm:inline-flex items-center space-x-1.5 rounded-full bg-indigo-950/80 border border-indigo-700/50 px-3 py-1 text-xs font-semibold text-indigo-300 hover:bg-indigo-900/60 hover:text-white transition-all cursor-pointer active:scale-95 select-none"
        >
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>Take Adaptive Diagnostic</span>
        </Link>

        {/* Due Reviews shortcut */}
        <Link
          href="/reviews"
          className="flex items-center space-x-1.5 text-xs text-slate-300 hover:text-white px-2.5 py-1.5 rounded-md border border-slate-800 bg-slate-900 hover:border-slate-700 transition-all cursor-pointer active:scale-95 select-none"
        >
          <span>🔄</span>
          <span className="hidden md:inline">Spaced Reviews</span>
        </Link>

        {/* User Dropdown */}
        <div className="relative">
          <button
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="flex items-center space-x-2.5 rounded-xl border border-slate-800 bg-slate-900/80 px-2.5 py-1.5 text-xs font-medium text-slate-200 hover:border-slate-700 hover:text-white transition-all cursor-pointer active:scale-95 select-none"
          >
            <div className="relative h-6 w-6 rounded-full bg-white p-0.5 border border-indigo-400/50 overflow-hidden flex-shrink-0">
              <img
                src="/images/knowpath-avatar.jpg"
                alt="Profile"
                className="h-full w-full rounded-full object-cover"
              />
            </div>
            <span className="max-w-[100px] sm:max-w-[140px] truncate">{user?.email || "Account"}</span>
            <svg className="h-3 w-3 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          {dropdownOpen && (
            <div className="absolute right-0 mt-2 w-56 rounded-2xl border border-slate-800 bg-slate-900 p-2 shadow-2xl z-50">
              <div className="flex items-center space-x-3 px-3 py-2.5 mb-2 rounded-xl bg-slate-950 border border-slate-800/80">
                <div className="h-9 w-9 rounded-full bg-white p-0.5 border border-indigo-500/50 overflow-hidden flex-shrink-0 shadow-sm">
                  <img
                    src="/images/knowpath-avatar.jpg"
                    alt="Profile Avatar"
                    className="h-full w-full rounded-full object-cover"
                  />
                </div>
                <div className="overflow-hidden">
                  <p className="text-xs font-semibold text-white truncate">{user?.email || "Learner"}</p>
                  <span className="inline-flex items-center text-[10px] text-emerald-400 font-medium">
                    <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 mr-1 animate-pulse"></span>
                    Verified Profile
                  </span>
                </div>
              </div>

              <Link
                href="/settings"
                onClick={() => setDropdownOpen(false)}
                className="flex items-center px-3 py-2 text-xs text-slate-300 hover:bg-slate-800 hover:text-white rounded-lg transition-colors cursor-pointer"
              >
                <span>⚙️ Settings & Data Export</span>
              </Link>
              <Link
                href="/disputes"
                onClick={() => setDropdownOpen(false)}
                className="flex items-center px-3 py-2 text-xs text-slate-300 hover:bg-slate-800 hover:text-white rounded-lg transition-colors cursor-pointer"
              >
                <span>⚖️ Disputes & Integrity</span>
              </Link>
              <div className="my-1 border-t border-slate-800"></div>
              <button
                onClick={() => {
                  setDropdownOpen(false);
                  handleSignOut();
                }}
                className="w-full text-left rounded-lg px-3 py-2 text-xs text-rose-400 hover:bg-rose-950/40 hover:text-rose-300 transition-colors cursor-pointer active:scale-98"
              >
                🚪 Sign Out
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
