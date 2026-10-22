#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PIDFILE=".hexcat_hcx_ui.pid"

# Clear a stale PID file. If that exact process is still alive, do not start a duplicate.
if [[ -f "$PIDFILE" ]]; then
  PID="$(tr -dc '0-9' < "$PIDFILE" || true)"
  if [[ -n "$PID" ]] && kill -0 "$PID" 2>/dev/null; then
    echo "HEXCAT HCX UI is already running (PID $PID)."
    exit 0
  fi
  rm -f "$PIDFILE"
fi

exec python3 HEXCAT4.py
