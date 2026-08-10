---
name: sub-graper
description: Delegate codebase search to an isolated subagent instead of grepping inline, cache resolved results per project, and manage invalidation of those results. Use whenever the user asks where something is implemented, how a flow works, to locate code, functions, handlers, or config across a repo, or to invalidate or clear Sub-Graper cache entries. Use before running grep/read/list_dir searches directly in the main conversation.
---

# Sub-Graper

A code-search skill that keeps search noise out of the main conversation and
remembers resolved answers per project so the next similar question is
instant.

## Why this exists

Searching a codebase directly in the main context burns tokens on dead ends:
failed greps, files that turned out to be irrelevant, false leads. This skill
moves that mess into an isolated subagent, and — because most codebase
questions repeat in some form over a project's life — keeps a lightweight,
per-project memory of what was already found, so the second time a similar
question comes up it costs nothing.

## Core contract

- Never grep/read/list_dir directly in the main conversation to answer a
  "where/how is X implemented" question. Always route through this skill —
  except for the trivial-case bypass below.
- Always check the project's cache before spawning a search subagent.
- Return a cache hit only when it is fresh, matches conservatively, every
  referenced file and line range still exists, and the content fingerprint
  still matches (see "Cache validation").
- A search is delegated to exactly **one** subagent per query. That subagent
  runs grep/read/list_dir calls in parallel within its own turns — never
  spawn multiple competing subagents for a single query.
- Cap the subagent at 3–4 turns. Stop earlier once a small set of spans
  looks conclusive.
- Only cache a search that resolved to confident, specific spans. Never
  cache an empty, uncertain, or "couldn't find it" result.
- Cache entries expire on a simple TTL (days), configured in `config.json`.
  Do not invalidate automatically from Git HEAD. Let the user invalidate one
  entry or clear the current project's cache when repository changes make
  cached results stale.
- Cache is scoped per project by repo root path, never by a display name
  from any external tool.
- Store cache data outside the installed skill directory. Resolve the cache
  root using `--cache-dir`, then `SUB_GRAPER_CACHE_DIR`, then `config.json`,
  and finally `<project-root>/.codex/sub-graper-cache`.
- A user flagging a bad result invalidates only that one cache entry, never
  the whole project cache, unless the user explicitly asks to clear it.

## Trivial-case bypass

Skip cache lookup and subagent delegation entirely when no actual search is
needed:

- the user already gave an exact file path (and, if relevant, line
  numbers) rather than asking where something is;
- the answer is already visible in the current conversation context (e.g.
  a file already read this turn).

In these cases, just answer directly. Routing a non-search through the
cache/subagent machinery adds overhead for no benefit. Anything short of
this — including "I think it's in the auth module, can you confirm" — still
goes through the normal working loop.

## Working loop

1. **Resolve the project key.**
   Run `git rev-parse --show-toplevel` from the current working directory.
   If that fails (not a git repo), use the absolute current working
   directory instead. This is the project key — never use a project name
   from Codex, Claude Code, or any other tool's UI.

2. **Check the cache first.**
   Resolve this skill's directory from the loaded `SKILL.md`, select an
   available Python 3 runtime, and run:

   ```
   <python> "<skill-dir>/scripts/sub_graper.py" lookup --project-root "<resolved path>" --query "<user's question, in your own words>"
   ```

   - If it returns a `HIT`, answer directly from the printed entry. Do not
     spawn a subagent.
   - If it returns `MISS` (no match, match expired per TTL, or match found
     but the content fingerprint no longer matches), continue to step 3.
   - If the command errors (script failure, corrupted cache, missing
     Python), retry once. If it fails again, treat this as a full cache
     outage for the current query: skip straight to step 3 as a direct,
     uncached search, and don't attempt to write a cache entry afterward
     unless a later lookup succeeds cleanly.

3. **Delegate the search to one subagent.**
   Spawn a single search subagent (e.g. via the Task tool) with a prompt
   along these lines:

   > Search this repository to answer: "<query>". Run grep, read, and
   > list_dir calls in parallel where possible. You have at most 4 turns.
   > Stop as soon as you have a small, confident set of file:line-range
   > spans that answer the question — at most 8 spans; if more genuinely
   > apply, return the 8 most representative and say so. Return ONLY:
   > (a) the resolved file:line-range spans, (b) one sentence per span on
   > why it matches, and (c) a confidence level (confident / uncertain /
   > not found). Do not return raw grep output, dead ends, or your search
   > process. If you reach your turn limit without a confident or
   > not-found conclusion, return your best partial spans with confidence
   > "uncertain" rather than continuing further.

4. **Handle the subagent's result.**
   - If confidence is **confident**: write it to the cache (step 5), then
     answer the user from it.
   - If confidence is **uncertain** or **not found** — including the case
     where the subagent hit its turn cap without resolving — answer the
     user honestly, noting the search was inconclusive, but do **not**
     write anything to the cache.

5. **Write to cache (confident results only).**
   Run:
   ```
   <python> "<skill-dir>/scripts/sub_graper.py" write --project-root "<resolved path>" --query "<query>" --spans "<file:line-range spans, one per line>" --notes "<why each span matched>"
   ```
   This creates one entry file under the project's cache folder and
   appends one JSON object to that project's `index.jsonl`, including a
   content fingerprint (see "Cache validation") for each span. The command
   refuses to cache missing files, malformed spans, or invalid line ranges.

## Handling corrections

If the user says a returned result was wrong or outdated:

```
<python> "<skill-dir>/scripts/sub_graper.py" invalidate --project-root "<resolved path>" --entry "<entry slug or exact query text>"
```

Matching for invalidation is exact, not fuzzy — it matches an exact entry
slug or the exact original query text, not a token-overlap approximation
like lookup uses. If the given text doesn't exactly match a single entry:

- **no match** — report that nothing matched and ask the user to confirm
  the query or slug (e.g. by listing recent entries for the project);
- **multiple matches** — list the candidate entries (query text and
  spans) and ask the user which one to invalidate before removing anything.

Never guess and invalidate the "closest" entry.

Only run a full wipe —

```
<python> "<skill-dir>/scripts/sub_graper.py" clear --project-root "<resolved path>"
```

— if the user explicitly asks to clear the whole project's cache.

## Cache validation

Before returning a hit, a cached entry must pass all of the following, in
order. A failed check at any point is a miss:

1. **Freshness** — the entry is within `ttl_days` of its creation date.
2. **Query match** — conservative keyword overlap between the new query and
   the cached entry's query text. Non-identical queries must share at
   least two meaningful tokens and meet `similarity_threshold` from
   `config.json`. Treat weak matches as misses rather than risk returning
   unrelated code.
3. **Structural validity** — every cached span uses `path:start-end`
   format, remains inside the project root, references an existing file,
   and does not exceed the file's current line count.
4. **Content fingerprint** — the cached entry stores a hash of each span's
   text at write time. On lookup, re-read the span at its recorded line
   range and recompute the hash. If it doesn't match, the underlying code
   has changed since caching (even if the line range still looks valid in
   isolation) — treat as a miss.

## Configuration

`config.json` in this skill's folder:

```json
{
  "ttl_days": 14,
  "cache_dir": null,
  "similarity_threshold": 0.6
}
```

Change `ttl_days` to adjust how long results remain fresh. Set `cache_dir`
to an absolute path or a path relative to the project root. Set
`similarity_threshold` to control how strict query matching is (higher =
stricter; used alongside the two-shared-token minimum in "Cache
validation"). Prefer the `SUB_GRAPER_CACHE_DIR` environment variable for a
user-level override and `--cache-dir` for a one-command override.

## File layout this skill creates

```
<cache-root>/
  <project-key-hash>-<project-basename>/
    index.jsonl             (one JSON object per entry, incl. span fingerprints)
    entries/
      <query-slug>.md       (query, spans, notes, created date)
```

## What not to do

- Do not spawn more than one subagent per query — that duplicates context
  setup cost for no benefit over parallel tool calls within one subagent.
- Do not cache a result you are not confident in.
- Do not return a cached entry whose files, line ranges, or content
  fingerprints fail validation.
- Do not key the cache by a project name from an external tool's UI —
  those are not stable or reliably readable.
- Do not silently drop the whole project cache on a single bad result.
- Do not invalidate an entry on a fuzzy or ambiguous match — require an
  exact match or ask the user to disambiguate.
- Do not route a trivial, no-search-needed case through cache lookup or
  subagent delegation.
