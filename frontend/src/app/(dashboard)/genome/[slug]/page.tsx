import React from "react";
import ConceptDetailView from "./ConceptDetailView";

const ALL_CONCEPT_SLUGS = [
  "variables-basics", "data-types-overview", "integers", "floats", "strings-basics",
  "booleans", "none-type", "print-function", "input-function", "comments",
  "arithmetic-operators", "comparison-operators", "logical-operators", "string-formatting",
  "string-methods", "string-indexing", "string-operations", "string-immutability",
  "type-conversion", "if-statements", "elif-else", "while-loops", "range-function",
  "for-loops", "break-continue", "nested-loops", "lists-basics", "list-methods",
  "list-slicing", "list-comprehensions", "tuples", "sets", "dicts-basics",
  "dict-methods", "dict-comprehensions", "nested-data", "functions-basics",
  "function-parameters", "default-arguments", "keyword-arguments", "return-values",
  "variable-scope", "lambda-functions", "args-kwargs", "higher-order-functions",
  "recursion", "regular-expressions-intro", "file-reading", "file-writing",
  "file-context-managers", "file-paths", "exceptions-basics", "try-except",
  "exception-types", "raising-exceptions", "finally-else", "custom-exceptions",
  "oop-concepts", "classes-basics", "constructors", "instance-methods",
  "class-attributes", "encapsulation", "inheritance", "method-overriding",
  "special-methods", "complexity-basics", "linear-search", "binary-search",
  "bubble-sort", "selection-sort", "insertion-sort", "recursion-algorithms",
  "two-pointer", "sliding-window", "generators", "decorators",
  "modules-packages", "standard-library"
];

export async function generateStaticParams() {
  return ALL_CONCEPT_SLUGS.map((slug) => ({
    slug,
  }));
}

export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  return <ConceptDetailView slug={slug} />;
}
