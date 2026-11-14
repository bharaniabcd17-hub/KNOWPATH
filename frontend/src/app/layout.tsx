import type { Metadata } from "next";
import "@/styles/globals.css";

export const metadata: Metadata = {
  title: "KNOWPATH | Evidence-Based Learner Intelligence Platform",
  description: "Model what a learner demonstrably knows, find gaps, recommend the next action, always explainably.",
  icons: {
    icon: "/images/knowpath-logo.jpg",
    apple: "/images/knowpath-avatar.jpg",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-[var(--color-bg)] text-[var(--color-fg)] antialiased font-sans">
        {children}
      </body>
    </html>
  );
}
