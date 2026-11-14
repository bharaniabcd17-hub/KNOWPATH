"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter, usePathname } from "next/navigation";
import { useAuthStore } from "@/stores/auth";

const NAV_LINKS = [
  { name: "Features", href: "/features" },
  { name: "How It Works", href: "/how-it-works" },
  { name: "For Students", href: "/for-students" },
  { name: "For Professionals", href: "/for-professionals" },
  { name: "About", href: "/about" },
  { name: "Contact", href: "/contact" },
];

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const { user, token, logout, checkAuth } = useAuthStore();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 15);
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const handleLogout = async () => {
    await logout();
    router.push("/");
  };

  return (
    <header
      className={`sticky top-0 z-50 w-full px-3 sm:px-6 lg:px-8 transition-all duration-300 ${
        scrolled ? "pt-2 pb-2" : "pt-3 sm:pt-4 pb-2"
      }`}
    >
      {/* Floating Glass Navigation Bar Container */}
      <div
        className={`mx-auto max-w-7xl rounded-2xl transition-all duration-300 relative border ${
          scrolled
            ? "bg-slate-950/85 backdrop-blur-2xl border-white/[0.10] shadow-2xl shadow-black/60 ring-1 ring-white/[0.04]"
            : "bg-slate-950/60 backdrop-blur-xl border-white/[0.07] shadow-xl shadow-black/30"
        } px-4 sm:px-6 h-16 flex items-center justify-between`}
      >
        {/* Subtle Specular Top Reflection Glare */}
        <div
          className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-cyan-400/25 to-transparent rounded-t-2xl pointer-events-none"
          aria-hidden="true"
        />

        {/* LEFT: Logo & EVOLVE v1.0 Badge */}
        <Link
          href="/"
          className="flex items-center space-x-3 group cursor-pointer active:scale-98 transition-transform select-none"
        >
          <div className="relative flex h-9 w-9 items-center justify-center rounded-xl bg-white p-0.5 shadow-md shadow-cyan-500/10 border border-cyan-400/30 overflow-hidden flex-shrink-0 group-hover:scale-105 group-hover:border-cyan-400/50 transition-all duration-200">
            <img
              src="/images/knowpath-logo.jpg"
              alt="KNOWPATH"
              className="h-full w-full object-contain"
            />
          </div>
          <div className="flex items-center">
            <span className="text-base sm:text-lg font-extrabold tracking-tight text-white group-hover:text-slate-100 transition-colors">
              KNOW<span className="text-cyan-400">PATH</span>
            </span>
            <span className="hidden sm:inline-flex items-center space-x-1 ml-2.5 rounded-full bg-cyan-950/60 border border-cyan-500/30 px-2 py-0.5 text-[10px] font-semibold tracking-wide text-cyan-300 shadow-sm">
              <span className="h-1.5 w-1.5 rounded-full bg-cyan-400 animate-pulse"></span>
              <span>EVOLVE v1.0</span>
            </span>
          </div>
        </Link>

        {/* CENTER: Navigation Links */}
        <nav className="hidden md:flex items-center space-x-1 lg:space-x-1.5 text-xs lg:text-sm font-medium">
          {NAV_LINKS.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`relative px-3 lg:px-3.5 py-1.5 rounded-lg transition-all duration-200 select-none cursor-pointer ${
                  isActive
                    ? "text-white font-semibold"
                    : "text-slate-300 hover:text-white hover:bg-white/[0.04]"
                }`}
              >
                <span>{link.name}</span>
                {isActive && (
                  <span
                    className="absolute bottom-0 left-3 right-3 h-[2px] bg-gradient-to-r from-cyan-400 via-sky-400 to-indigo-500 rounded-full shadow-[0_0_8px_rgba(34,211,238,0.7)]"
                    aria-hidden="true"
                  />
                )}
              </Link>
            );
          })}
        </nav>

        {/* RIGHT: CTA Action Buttons */}
        <div className="hidden md:flex items-center space-x-3">
          {token && user ? (
            <div className="flex items-center space-x-2.5">
              <Link
                href="/dashboard"
                className="relative inline-flex items-center space-x-2 rounded-xl bg-gradient-to-r from-blue-600 via-indigo-600 to-cyan-500 px-4 py-2 text-xs sm:text-sm font-semibold text-white shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/35 hover:from-blue-500 hover:to-cyan-400 transition-all duration-200 active:scale-95 cursor-pointer select-none"
              >
                <span className="h-1.5 w-1.5 rounded-full bg-cyan-300 animate-pulse"></span>
                <span>Go to Dashboard</span>
              </Link>
              <button
                onClick={handleLogout}
                className="rounded-xl border border-white/[0.08] bg-slate-900/80 px-3.5 py-2 text-xs sm:text-sm font-medium text-slate-300 hover:bg-white/[0.06] hover:text-white transition-all duration-200 cursor-pointer active:scale-95 select-none"
              >
                Sign Out
              </button>
            </div>
          ) : (
            <div className="flex items-center space-x-2">
              <Link
                href="/login"
                className="text-xs sm:text-sm font-medium text-slate-300 hover:text-white px-3.5 py-2 rounded-xl transition-all duration-200 hover:bg-white/[0.06] active:scale-95 cursor-pointer select-none"
              >
                Sign In
              </Link>
              <Link
                href="/register"
                className="relative inline-flex items-center justify-center rounded-xl bg-gradient-to-r from-blue-600 via-indigo-600 to-cyan-500 px-4 py-2 text-xs sm:text-sm font-semibold text-white shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/35 hover:from-blue-500 hover:to-cyan-400 transition-all duration-200 active:scale-95 cursor-pointer select-none overflow-hidden group"
              >
                <span
                  className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"
                  aria-hidden="true"
                />
                <span>Get Started</span>
              </Link>
            </div>
          )}
        </div>

        {/* Mobile Menu Toggle Button */}
        <div className="flex md:hidden">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="rounded-xl p-2 text-slate-300 hover:text-white hover:bg-white/[0.08] border border-white/[0.06] transition-all duration-150 cursor-pointer active:scale-95"
            aria-label="Toggle mobile navigation menu"
            aria-expanded={mobileMenuOpen}
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {mobileMenuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Floating Glass Dropdown Panel */}
      {mobileMenuOpen && (
        <div className="md:hidden mx-auto max-w-7xl mt-2 rounded-2xl border border-white/[0.10] bg-slate-950/95 backdrop-blur-2xl p-4 shadow-2xl shadow-black/80 animate-in slide-in-from-top-2 duration-200">
          <nav className="flex flex-col space-y-1 text-sm font-medium text-slate-300">
            {NAV_LINKS.map((link) => {
              const isActive = pathname === link.href;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`flex items-center justify-between px-3.5 py-2.5 rounded-xl transition-all duration-150 cursor-pointer active:scale-98 ${
                    isActive
                      ? "bg-cyan-950/40 text-cyan-300 border border-cyan-500/30 font-semibold"
                      : "hover:bg-white/[0.05] hover:text-white"
                  }`}
                >
                  <span>{link.name}</span>
                  {isActive && (
                    <span className="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
                  )}
                </Link>
              );
            })}

            <div className="pt-3 mt-1 border-t border-white/[0.08] flex flex-col space-y-2">
              {token && user ? (
                <>
                  <Link
                    href="/dashboard"
                    onClick={() => setMobileMenuOpen(false)}
                    className="w-full text-center rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 py-3 font-semibold text-white shadow-lg shadow-cyan-500/20 transition-all cursor-pointer active:scale-98"
                  >
                    Go to Dashboard
                  </Link>
                  <button
                    onClick={() => {
                      setMobileMenuOpen(false);
                      handleLogout();
                    }}
                    className="w-full text-center rounded-xl border border-white/[0.08] bg-slate-900 py-3 font-medium text-slate-300 hover:text-white transition-all cursor-pointer active:scale-98"
                  >
                    Sign Out
                  </button>
                </>
              ) : (
                <>
                  <Link
                    href="/login"
                    onClick={() => setMobileMenuOpen(false)}
                    className="w-full text-center rounded-xl border border-white/[0.08] bg-slate-900/80 py-3 font-medium text-slate-300 hover:text-white transition-all cursor-pointer active:scale-98"
                  >
                    Sign In
                  </Link>
                  <Link
                    href="/register"
                    onClick={() => setMobileMenuOpen(false)}
                    className="w-full text-center rounded-xl bg-gradient-to-r from-blue-600 via-indigo-600 to-cyan-500 py-3 font-semibold text-white shadow-lg shadow-cyan-500/25 transition-all cursor-pointer active:scale-98"
                  >
                    Get Started
                  </Link>
                </>
              )}
            </div>
          </nav>
        </div>
      )}
    </header>
  );
}
