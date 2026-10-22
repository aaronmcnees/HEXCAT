#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PIDFILE=".hexcat_hcx_ui.pid"
SCRIPT="$PWD/HEXCAT4.py"
STOPPED=0

if [[ -f "$PIDFILE" ]]; then
  PID="$(tr -dc '0-9' < "$PIDFILE" || true)"
  if [[ -n "$PID" ]] && kill -0 "$PID" 2>/dev/null; then
    echo "Stopping HEXCAT HCX UI (PID $PID)..."
    kill -INT "$PID" 2>/dev/null || true
    for _ in {1..30}; do
      kill -0 "$PID" 2>/dev/null || break
      sleep 0.1
    done
    if kill -0 "$PID" 2>/dev/null; then
      kill -TERM "$PID" 2>/dev/null || true
    fi
    STOPPED=1
  fi
  rm -f "$PIDFILE"
fi

# Compatibility cleanup for the previous build, which did not create a PID file.
while IFS= read -r PID; do
  [[ -z "$PID" || "$PID" == "$$" ]] && continue
  CMD="$(ps -p "$PID" -o args= 2>/dev/null || true)"
  if [[ "$CMD" == *"HEXCAT4.py"* ]]; then
    echo "Stopping older wrapper process (PID $PID)..."
    kill -INT "$PID" 2>/dev/null || true
    STOPPED=1
  fi
done < <(pgrep -f 'python3 .*HEXCAT4\.py' 2>/dev/null || true)

if [[ "$STOPPED" -eq 0 ]]; then
  echo "HEXCAT HCX UI is not running."
else
  echo "Stopped."
fi
