"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { AssessmentItem, SubmitAnswerResponse } from "@/types";

export default function DiagnosticRunnerPage() {
  const [attemptId, setAttemptId] = useState<string | null>(null);
  const [currentItem, setCurrentItem] = useState<AssessmentItem | null>(null);
  const [itemIndex, setItemIndex] = useState(1);
  const [selectedOption, setSelectedOption] = useState<string>("");
  const [selectedMulti, setSelectedMulti] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [lastResult, setLastResult] = useState<SubmitAnswerResponse | null>(null);
  const [startTime, setStartTime] = useState<number>(Date.now());
  const [finished, setFinished] = useState(false);
  const [history, setHistory] = useState<{ is_correct: boolean; concept_id: string }[]>([]);

  useEffect(() => {
    const start = async () => {
      try {
        setLoading(true);
        const res = await api.startDiagnostic("diagnostic");
        setAttemptId(res.attempt_id);
        setCurrentItem(res.first_item);
        setStartTime(Date.now());
      } catch (err) {
        console.error("Diagnostic start error:", err);
      } finally {
        setLoading(false);
      }
    };
    start();
  }, []);

  const handleSelectOption = (key: string) => {
    if (!currentItem) return;
    if (currentItem.kind === "multi_select") {
      if (selectedMulti.includes(key)) {
        setSelectedMulti(selectedMulti.filter((k) => k !== key));
      } else {
        setSelectedMulti([...selectedMulti, key]);
      }
    } else {
      setSelectedOption(key);
    }
  };

  const handleSubmit = async () => {
    if (!attemptId || !currentItem) return;

    let answerStr = selectedOption;
    if (currentItem.kind === "multi_select") {
      if (selectedMulti.length === 0) return;
      answerStr = [...selectedMulti].sort().join(",");
    } else {
      if (!selectedOption) return;
    }

    setSubmitting(true);
    const timeMs = Date.now() - startTime;

    try {
      const res = await api.submitAnswer({
        attempt_id: attemptId,
        question_id: currentItem.id,
        answer: answerStr,
        time_ms: timeMs,
      });

      setLastResult(res);
      setHistory((prev) => [...prev, { is_correct: res.is_correct, concept_id: currentItem.concept_id }]);

      if (res.is_completed || !res.next_item) {
        setFinished(true);
      }
    } catch (err) {
      console.error("Answer submission error:", err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleNextQuestion = () => {
    if (!lastResult?.next_item) {
      setFinished(true);
      return;
    }
    setCurrentItem(lastResult.next_item);
    setLastResult(null);
    setSelectedOption("");
    setSelectedMulti([]);
    setItemIndex((prev) => prev + 1);
    setStartTime(Date.now());
  };

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="flex items-center space-x-3 text-slate-400">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent"></div>
          <span className="text-sm">Initializing adaptive diagnostic session...</span>
        </div>
      </div>
    );
  }

  if (finished) {
    const correctCount = history.filter((h) => h.is_correct).length;
    const totalCount = history.length;
    const accuracy = totalCount > 0 ? (correctCount / totalCount) * 100 : 0;

    return (
      <div className="max-w-2xl mx-auto rounded-3xl border border-slate-800 bg-slate-900/60 p-8 sm:p-12 text-center space-y-6">
        <div className="inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-indigo-600/20 border border-indigo-500/40 text-3xl">
          🎯
        </div>

        <h1 className="text-3xl font-extrabold text-white">Diagnostic Session Completed</h1>
        <p className="text-sm text-slate-300 max-w-md mx-auto leading-relaxed">
          Your answers have been ingested into the Bayesian scoring engine. Evidence weights and credible intervals
          have been updated across all affected concepts.
        </p>

        <div className="grid grid-cols-3 gap-4 max-w-sm mx-auto p-4 rounded-xl bg-slate-950 border border-slate-800">
          <div>
            <div className="text-xs text-slate-500">Items Answered</div>
            <div className="text-2xl font-bold text-white mt-1">{totalCount}</div>
          </div>
          <div>
            <div className="text-xs text-slate-500">Correct</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">{correctCount}</div>
          </div>
          <div>
            <div className="text-xs text-slate-500">Accuracy</div>
            <div className="text-2xl font-bold text-indigo-400 mt-1">{accuracy.toFixed(0)}%</div>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
          <Link
            href="/twin"
            className="w-full sm:w-auto rounded-xl bg-indigo-600 px-6 py-3 text-sm font-semibold text-white hover:bg-indigo-500 transition-colors"
          >
            Inspect Updated Cognitive Twin →
          </Link>
          <Link
            href="/roadmap"
            className="w-full sm:w-auto rounded-xl border border-slate-700 bg-slate-950 px-6 py-3 text-sm font-semibold text-slate-300 hover:text-white transition-colors"
          >
            View Adaptive Roadmap
          </Link>
        </div>
      </div>
    );
  }

  if (!currentItem) {
    return (
      <div className="text-center py-12 text-slate-400">
        <p>No active assessment item available.</p>
        <Link href="/dashboard" className="text-indigo-400 underline mt-2 inline-block">
          Return to Dashboard
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Top Progress & Concept Indicator */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-3">
          <span className="rounded bg-indigo-950 border border-indigo-700/60 px-2.5 py-1 text-xs font-bold text-indigo-300">
            Question #{itemIndex}
          </span>
          <span className="text-xs text-slate-400 font-mono">
            Concept: <span className="text-slate-200">{currentItem.concept_id}</span>
          </span>
        </div>

        <div className="flex items-center space-x-2">
          <span className="capitalize text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-medium">
            {currentItem.kind.replace("_", " ")}
          </span>
          <span className="capitalize text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-medium">
            {currentItem.difficulty}
          </span>
        </div>
      </div>

      {/* Main Question Card */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 sm:p-8 space-y-6 shadow-xl">
        <h2 className="text-base sm:text-lg font-bold text-white leading-relaxed">
          {currentItem.stem}
        </h2>

        {/* Optional Code Snippet */}
        {currentItem.code_snippet && (
          <div className="rounded-xl border border-slate-800 bg-slate-950 p-4 font-mono text-xs text-indigo-300 overflow-x-auto">
            <pre>{currentItem.code_snippet}</pre>
          </div>
        )}

        {/* Options List */}
        <div className="space-y-3 pt-2">
          {currentItem.options?.map((opt) => {
            const isSelected =
              currentItem.kind === "multi_select"
                ? selectedMulti.includes(opt.key)
                : selectedOption === opt.key;

            return (
              <button
                key={opt.key}
                type="button"
                disabled={lastResult !== null}
                onClick={() => handleSelectOption(opt.key)}
                className={`w-full text-left p-4 rounded-xl border text-xs sm:text-sm transition-all flex items-start space-x-3 ${
                  isSelected
                    ? "border-indigo-500 bg-indigo-950/40 text-white font-medium"
                    : "border-slate-800 bg-slate-950/80 text-slate-300 hover:border-slate-700 hover:bg-slate-900"
                } ${lastResult !== null ? "cursor-default" : "cursor-pointer"}`}
              >
                <span
                  className={`flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-lg text-xs font-bold ${
                    isSelected ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400"
                  }`}
                >
                  {opt.key}
                </span>
                <span className="pt-0.5 flex-1">{opt.text}</span>
              </button>
            );
          })}
        </div>

        {/* Feedback Alert on Submit */}
        {lastResult && (
          <div
            className={`p-4 rounded-xl border text-xs leading-relaxed space-y-2 ${
              lastResult.is_correct
                ? "bg-emerald-950/30 border-emerald-900/60 text-emerald-200"
                : "bg-rose-950/30 border-rose-900/60 text-rose-200"
            }`}
          >
            <div className="flex items-center space-x-2 font-bold text-sm">
              <span>{lastResult.is_correct ? "✓ Correct Answer" : "✗ Incorrect Answer"}</span>
              <span className="text-[11px] font-normal text-slate-400">
                (Updated Mastery: {(lastResult.updated_mastery * 100).toFixed(0)}%)
              </span>
            </div>

            {lastResult.explanation && (
              <p className="text-slate-300">{lastResult.explanation}</p>
            )}

            {/* Misconception Trap Alert */}
            {lastResult.misconception_detected && (
              <div className="mt-3 p-3 rounded-lg bg-amber-950/50 border border-amber-800/80 text-amber-200 text-xs">
                <span className="font-bold block mb-1">⚠️ Misconception Detected:</span>
                <span>{lastResult.misconception_detected}</span>
              </div>
            )}
          </div>
        )}

        {/* Actions Button */}
        <div className="pt-4 border-t border-slate-800 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          <div className="text-xs text-slate-400">
            {currentItem.kind === "multi_select"
              ? "Select all correct options"
              : "Choose one option and submit"}
          </div>

          <div>
            {!lastResult ? (
              <button
                onClick={handleSubmit}
                disabled={
                  submitting ||
                  (currentItem.kind === "multi_select" ? selectedMulti.length === 0 : !selectedOption)
                }
                className="w-full sm:w-auto rounded-xl bg-indigo-600 px-6 py-3 text-xs sm:text-sm font-semibold text-white shadow-md hover:bg-indigo-500 disabled:opacity-50 transition-all cursor-pointer active:scale-95 disabled:cursor-not-allowed select-none"
              >
                {submitting ? "Grading..." : "Submit Answer"}
              </button>
            ) : (
              <button
                onClick={handleNextQuestion}
                className="w-full sm:w-auto rounded-xl bg-teal-600 px-6 py-3 text-xs sm:text-sm font-semibold text-white shadow-md hover:bg-teal-500 transition-all cursor-pointer active:scale-95 select-none"
              >
                Next Item →
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
