---
name: sub-graper
description: Perform a bounded, isolated codebase search after sub-router determines delegation is worthwhile. Use for broad or uncertain code-location and implementation-flow questions; do not use for direct, simple lookups.
---

# Sub-Graper

Search a codebase in an isolated subagent only after `sub-router` has selected
this skill. Return decisive code locations without exposing search noise to the
main conversation.

## Core contract

- Do not decide whether to delegate. `sub-router` owns that decision.
- Receive a compact task contract: objective, relevant paths, hard turn/tool
  budget, desired output shape, and stop condition.
- Use exactly one search subagent. Do not create competing searches for the
  same question.
- Start with one search turn. Allow one follow-up only when the first turn is
  inconclusive and a specific next check could change the answer.
- Stop once a small, confident set of spans answers the question. Return at
  most three spans by default; return up to five only when the question needs
  them.
- Return only file:line spans, a short reason for each, and a confidence level.
  Omit raw grep output, dead ends, and search narration.
- Cache only confident, specific results that the caller expects to reuse.
  Never cache an uncertain or not-found result.

## Working loop

1. Confirm the routed objective and bounds. If the contract is incomplete,
   return the missing field instead of broadening the search.
2. Check session-local knowledge first. A result already established in this
   conversation should be returned directly without a cache process or a new
   subagent.
3. Consult the durable cache only when the caller requests it or the answer is
   likely to recur. Resolve the project root once per session and use
   `scripts/sub_graper.py lookup`. If the cache is unavailable, mark it
   unavailable for the session and continue uncached; do not retry it for each
   later query.
4. Delegate one targeted search with the supplied budget. Search the named
   paths first, use focused file discovery and text search, then read only the
   candidate spans needed to answer.
5. If the result is confident, return it and optionally write it to the durable
   cache when reuse is likely. Otherwise return the best partial result as
   `uncertain` or `not found`; do not cache it.

## Search prompt shape

Give the search subagent only this information:

```text
Objective: <the code question>
Relevant paths: <paths, or "unknown">
Budget: <one turn; one follow-up only if a named check remains>
Output: <up to three file:line spans, reason, confidence>
Stop: <the condition that makes the answer sufficient>
```

Do not forward the full main conversation by default. Include only facts that
change the search, such as a known symbol, error, repository convention, or
already-eliminated location.

## Cache use

The durable cache is an optional reuse optimization, not a mandatory preflight.
Use it for recurring code-navigation questions or when the user asks for a
cached lookup. Before returning a hit, verify its TTL, query match, file paths,
and line ranges. Treat any failed check as a miss.

When caching a confident result, use `scripts/sub_graper.py write` with the
resolved project root, concise normalized query, spans, and notes. Keep cache
entries project-scoped. For a correction, invalidate only the exact entry; a
project-wide clear requires an explicit user request.

## What not to do

- Do not invoke this skill before `sub-router` decides that isolated search
  saves more work than its setup cost.
- Do not run an unbounded exploratory search or consume turns merely to be
  exhaustive.
- Do not use a durable cache for one-off questions by default.
- Do not expose raw search output or full agent reasoning to the caller.
- Do not invalidate a cache entry based on a fuzzy or ambiguous query.
