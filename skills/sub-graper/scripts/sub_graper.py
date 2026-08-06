#!/usr/bin/env python3
"""Manage Sub-Graper's per-project code-search cache."""

import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timedelta, timezone

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(SKILL_DIR, "config.json")
CACHE_ENV_VAR = "SUB_GRAPER_CACHE_DIR"
DEFAULT_TTL_DAYS = 14
MATCH_THRESHOLD = 0.6
MIN_SHARED_TOKENS = 2
DATE_FMT = "%Y-%m-%d"

STOPWORDS = {
    "a", "an", "the", "is", "are", "how", "does", "do", "in", "of", "to",
    "for", "and", "or", "on", "at", "it", "this", "that", "with", "where",
    "what", "which", "code", "find", "locate", "search",
}


def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            config = json.load(file)
        return config if isinstance(config, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def load_ttl_days(config=None):
    try:
        ttl_days = int((config or load_config()).get("ttl_days", DEFAULT_TTL_DAYS))
        return ttl_days if ttl_days >= 0 else DEFAULT_TTL_DAYS
    except (TypeError, ValueError):
        return DEFAULT_TTL_DAYS


def resolve_cache_root(project_root, explicit_cache_dir=None, config=None):
    """Resolve cache root by CLI flag, environment, config, then local default."""
    project_root = os.path.abspath(project_root)
    configured = (config or load_config()).get("cache_dir")
    requested = explicit_cache_dir or os.environ.get(CACHE_ENV_VAR) or configured

    if requested:
        cache_root = os.path.expandvars(os.path.expanduser(str(requested)))
        if not os.path.isabs(cache_root):
            cache_root = os.path.join(project_root, cache_root)
    else:
        cache_root = os.path.join(project_root, ".codex", "sub-graper-cache")

    return os.path.abspath(cache_root)


def slugify(text, max_len=50):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:max_len] or "query"


def project_key(project_root):
    project_root = os.path.abspath(project_root)
    digest = hashlib.sha1(project_root.encode("utf-8")).hexdigest()[:8]
    base = slugify(os.path.basename(project_root.rstrip(os.sep)) or "project", 30)
    return f"{digest}-{base}"


def project_dir(project_root, cache_root):
    return os.path.join(cache_root, project_key(project_root))


def index_path(project_root, cache_root):
    return os.path.join(project_dir(project_root, cache_root), "index.jsonl")


def entries_dir(project_root, cache_root):
    return os.path.join(project_dir(project_root, cache_root), "entries")


def tokenize(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {word for word in words if word not in STOPWORDS and len(word) > 1}


def match_score(query_a, query_b):
    tokens_a, tokens_b = tokenize(query_a), tokenize(query_b)
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = tokens_a & tokens_b
    if tokens_a != tokens_b and len(intersection) < MIN_SHARED_TOKENS:
        return 0.0
    return len(intersection) / len(tokens_a | tokens_b)


def read_index_entries(project_root, cache_root):
    path = index_path(project_root, cache_root)
    if not os.path.exists(path):
        return []

    entries = []
    with open(path, "r", encoding="utf-8") as file:
        for raw_line in file:
            if not raw_line.strip():
                continue
            try:
                entry = json.loads(raw_line)
            except json.JSONDecodeError:
                continue
            required = ("date", "slug", "query", "path")
            if isinstance(entry, dict) and all(
                isinstance(entry.get(key), str) for key in required
            ):
                entries.append({key: entry[key] for key in required})
    return entries


def write_index_entries(project_root, cache_root, entries):
    path = index_path(project_root, cache_root)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    temporary_path = path + ".tmp"
    with open(temporary_path, "w", encoding="utf-8", newline="\n") as file:
        for entry in entries:
            file.write(json.dumps(entry, ensure_ascii=False) + "\n")
    os.replace(temporary_path, path)


def is_expired(date_text, ttl_days):
    try:
        created = datetime.strptime(date_text, DATE_FMT).replace(tzinfo=timezone.utc)
    except ValueError:
        return True
    return datetime.now(timezone.utc) - created > timedelta(days=ttl_days)


def resolve_entry_file(project_root, cache_root, relative_path):
    if os.path.isabs(relative_path):
        return None
    cache_project_dir = os.path.abspath(project_dir(project_root, cache_root))
    full_path = os.path.abspath(
        os.path.join(cache_project_dir, *relative_path.split("/"))
    )
    try:
        if os.path.commonpath([cache_project_dir, full_path]) != cache_project_dir:
            return None
    except ValueError:
        return None
    return full_path


def normalize_span_lines(lines):
    return [
        line.strip().removeprefix("- ").strip().strip("`")
        for line in lines
        if line.strip()
    ]


def read_cached_spans(entry_file):
    spans = []
    in_spans = False
    try:
        with open(entry_file, "r", encoding="utf-8") as file:
            for raw_line in file:
                line = raw_line.strip()
                if line == "## Spans":
                    in_spans = True
                    continue
                if in_spans and line.startswith("## "):
                    break
                if in_spans and line:
                    spans.append(line)
    except OSError:
        return []
    return normalize_span_lines(spans)


def validate_span(project_root, span):
    match = re.fullmatch(r"(.+):(\d+)(?:-(\d+))?", span)
    if not match:
        return False, f"unrecognized span format: {span}"

    path_text, start_text, end_text = match.groups()
    project_root = os.path.abspath(project_root)
    candidate = os.path.expanduser(path_text.strip().strip('"'))
    full_path = candidate if os.path.isabs(candidate) else os.path.join(
        project_root, candidate
    )
    full_path = os.path.abspath(full_path)

    try:
        if os.path.commonpath([project_root, full_path]) != project_root:
            return False, f"span is outside the project: {span}"
    except ValueError:
        return False, f"span is outside the project: {span}"

    if not os.path.isfile(full_path):
        return False, f"file no longer exists: {path_text}"

    start = int(start_text)
    end = int(end_text or start_text)
    if start < 1 or end < start:
        return False, f"invalid line range: {span}"

    try:
        with open(full_path, "rb") as file:
            line_count = sum(1 for _ in file)
    except OSError:
        return False, f"file cannot be read: {path_text}"
    if end > line_count:
        return False, f"line range no longer exists: {span}"
    return True, ""


def validate_spans(project_root, spans):
    if not spans:
        return False, "entry has no parseable spans"
    for span in spans:
        valid, reason = validate_span(project_root, span)
        if not valid:
            return False, reason
    return True, ""


def validate_cached_entry(project_root, entry_file):
    if not entry_file or not os.path.isfile(entry_file):
        return False, "entry file is missing"
    return validate_spans(project_root, read_cached_spans(entry_file))


def cmd_lookup(args):
    config = load_config()
    ttl_days = load_ttl_days(config)
    cache_root = resolve_cache_root(args.project_root, args.cache_dir, config)
    entries = read_index_entries(args.project_root, cache_root)
    if not entries:
        print("MISS (no cache for this project)")
        return

    candidates = [
        (match_score(args.query, entry["query"]), entry) for entry in entries
    ]
    candidates = [item for item in candidates if item[0] >= MATCH_THRESHOLD]
    candidates.sort(key=lambda item: (item[0], item[1]["date"]), reverse=True)
    if not candidates:
        print("MISS (no sufficiently similar cached query)")
        return

    rejected = []
    for score, entry in candidates:
        if is_expired(entry["date"], ttl_days):
            rejected.append(f"{entry['slug']}: expired")
            continue
        entry_file = resolve_entry_file(args.project_root, cache_root, entry["path"])
        valid, reason = validate_cached_entry(args.project_root, entry_file)
        if not valid:
            rejected.append(f"{entry['slug']}: {reason}")
            continue

        print(
            f"HIT (score={score:.2f}, slug={entry['slug']}, "
            f"date={entry['date']})"
        )
        print(f"ENTRY_FILE: {entry_file}")
        print("---")
        with open(entry_file, "r", encoding="utf-8") as file:
            print(file.read())
        return

    print(f"MISS (matching cache entries were unusable: {'; '.join(rejected)})")


def cmd_write(args):
    cache_root = resolve_cache_root(args.project_root, args.cache_dir)
    cache_project_dir = project_dir(args.project_root, cache_root)
    entry_directory = entries_dir(args.project_root, cache_root)
    spans = normalize_span_lines(args.spans.splitlines())
    valid, reason = validate_spans(args.project_root, spans)
    if not valid:
        raise SystemExit(f"REFUSED TO CACHE ({reason})")

    os.makedirs(entry_directory, exist_ok=True)
    slug = slugify(args.query)
    entry_relative_path = f"entries/{slug}.md"
    entry_full_path = os.path.join(
        cache_project_dir, *entry_relative_path.split("/")
    )

    counter = 2
    base_slug = slug
    while os.path.exists(entry_full_path):
        slug = f"{base_slug}-{counter}"
        entry_relative_path = f"entries/{slug}.md"
        entry_full_path = os.path.join(
            cache_project_dir, *entry_relative_path.split("/")
        )
        counter += 1

    today = datetime.now(timezone.utc).strftime(DATE_FMT)
    with open(entry_full_path, "w", encoding="utf-8", newline="\n") as file:
        file.write(f"# {args.query.strip()}\n\n")
        file.write(f"Created: {today}\n\n")
        file.write("## Spans\n\n")
        file.write("\n".join(spans) + "\n\n")
        file.write("## Notes\n\n")
        file.write(f"{args.notes.strip()}\n")

    index_entry = {
        "date": today,
        "slug": slug,
        "query": args.query.strip(),
        "path": entry_relative_path,
    }
    index_file = index_path(args.project_root, cache_root)
    with open(index_file, "a", encoding="utf-8", newline="\n") as file:
        file.write(json.dumps(index_entry, ensure_ascii=False) + "\n")

    print(f"WROTE {entry_full_path}")


def cmd_invalidate(args):
    cache_root = resolve_cache_root(args.project_root, args.cache_dir)
    entries = read_index_entries(args.project_root, cache_root)
    if not entries:
        print("NOTHING TO INVALIDATE (no cache for this project)")
        return

    target = next((entry for entry in entries if entry["slug"] == args.entry), None)
    if target is None:
        matches = [
            (match_score(args.entry, entry["query"]), entry) for entry in entries
        ]
        matches = [item for item in matches if item[0] >= MATCH_THRESHOLD]
        if matches:
            target = max(matches, key=lambda item: item[0])[1]

    if target is None:
        print(f"NO MATCH for '{args.entry}', nothing invalidated")
        return

    remaining = [entry for entry in entries if entry["slug"] != target["slug"]]
    write_index_entries(args.project_root, cache_root, remaining)

    entry_file = resolve_entry_file(args.project_root, cache_root, target["path"])
    if entry_file and os.path.exists(entry_file):
        os.remove(entry_file)
    print(f"INVALIDATED {target['slug']}")


def cmd_clear(args):
    cache_root = resolve_cache_root(args.project_root, args.cache_dir)
    cache_project_dir = project_dir(args.project_root, cache_root)
    if not os.path.isdir(cache_project_dir):
        print("NOTHING TO CLEAR (no cache for this project)")
        return

    for root, directories, files in os.walk(cache_project_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in directories:
            os.rmdir(os.path.join(root, name))
    os.rmdir(cache_project_dir)
    print(f"CLEARED {cache_project_dir}")


def add_cache_argument(parser):
    parser.add_argument(
        "--cache-dir",
        help=(
            "Cache root override. Precedes SUB_GRAPER_CACHE_DIR and config.json."
        ),
    )


def main():
    parser = argparse.ArgumentParser(description="Sub-Graper cache manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    lookup = subparsers.add_parser("lookup")
    lookup.add_argument("--project-root", required=True)
    lookup.add_argument("--query", required=True)
    add_cache_argument(lookup)
    lookup.set_defaults(func=cmd_lookup)

    write = subparsers.add_parser("write")
    write.add_argument("--project-root", required=True)
    write.add_argument("--query", required=True)
    write.add_argument("--spans", required=True)
    write.add_argument("--notes", required=True)
    add_cache_argument(write)
    write.set_defaults(func=cmd_write)

    invalidate = subparsers.add_parser("invalidate")
    invalidate.add_argument("--project-root", required=True)
    invalidate.add_argument(
        "--entry", required=True, help="Exact entry slug or similar query text"
    )
    add_cache_argument(invalidate)
    invalidate.set_defaults(func=cmd_invalidate)

    clear = subparsers.add_parser("clear")
    clear.add_argument("--project-root", required=True)
    add_cache_argument(clear)
    clear.set_defaults(func=cmd_clear)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
