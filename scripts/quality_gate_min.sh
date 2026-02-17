#!/usr/bin/env bash
set -euo pipefail

OUT="${1:-ops/logs/precommit_quality_gate_manual.txt}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

ok=0
ng=0
warn=0

log() { echo "$*" | tee -a "$OUT" >/dev/null; }
pass() { log "PASS: $*"; ok=$((ok+1)); }
fail() { log "FAIL: $*"; ng=$((ng+1)); }
note() { log "WARN: $*"; warn=$((warn+1)); }

mkdir -p "$(dirname "$OUT")"
: > "$OUT"
log "[quality_gate_min] started: $(date '+%Y-%m-%d %H:%M:%S')"
log "[quality_gate_min] repo: $ROOT"

for f in "$ROOT/WORKFLOW.md" "$ROOT/agent.md" "$ROOT/README.md" "$ROOT/.gitignore"; do
  if [ -f "$f" ]; then pass "required file exists: $f"; else fail "missing required file: $f"; fi
done

if rg -n "TODO|TBD|___" "$ROOT/WORKFLOW.md" "$ROOT/agent.md" "$ROOT/README.md" >/tmp/t100_qg_todo.$$ 2>/dev/null; then
  fail "placeholders remain in core docs"
  cat /tmp/t100_qg_todo.$$ >> "$OUT"
else
  pass "no TODO/TBD/blank placeholders in core docs"
fi
rm -f /tmp/t100_qg_todo.$$ || true

if rg -n "ghp_[A-Za-z0-9]{20,}|-----BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY-----" \
  "$ROOT" -g '!.git/**' -g '!.venv/**' -g '!ops/logs/**' >/tmp/t100_qg_secret.$$ 2>/dev/null; then
  fail "potential secret patterns found"
  cat /tmp/t100_qg_secret.$$ >> "$OUT"
else
  pass "no obvious secret patterns"
fi
rm -f /tmp/t100_qg_secret.$$ || true

if [ "${RUN_PYTEST:-0}" = "1" ] && [ -x "$ROOT/.venv/bin/pytest" ]; then
  if "$ROOT/.venv/bin/pytest" -q >/tmp/t100_qg_pytest.$$ 2>&1; then
    pass "pytest passed"
  else
    fail "pytest failed"
    cat /tmp/t100_qg_pytest.$$ >> "$OUT"
  fi
  rm -f /tmp/t100_qg_pytest.$$ || true
else
  note "pytest skipped (set RUN_PYTEST=1 to enable)"
fi

log "SUMMARY: pass=$ok warn=$warn fail=$ng"
if [ "$ng" -gt 0 ]; then exit 1; fi
