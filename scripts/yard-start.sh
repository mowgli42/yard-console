#!/usr/bin/env bash
# Start the YARD live environment:
# 1. Background repos synchronizer (yard-sync)
# 2. Local HTTP server for the Tokyo Night console

set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

PORT="${PORT:-8000}"

echo "=========================================================="
echo " Starting YARD Mixed-Fleet Control Plane Live Environment"
echo "=========================================================="

# 1. Run initial sync to guarantee ~/.local/state/yard/status.json exists
python3 "$DIR/scripts/yard-sync.py"

# 2. Launch background sync daemon in watch mode (updates state every 5 seconds)
python3 "$DIR/scripts/yard-sync.py" --watch --interval 5 &
SYNC_PID=$!

cleanup() {
  echo ""
  echo "Shutting down YARD sync daemon (PID: $SYNC_PID)..."
  kill "$SYNC_PID" 2>/dev/null || true
  exit 0
}
trap cleanup SIGINT SIGTERM EXIT

echo "✓ yard-sync daemon running (PID: $SYNC_PID)"
echo "✓ Serving Tokyo Night Console on: http://localhost:$PORT"
echo "  Press Ctrl+C to stop."
echo "----------------------------------------------------------"

python3 -m http.server "$PORT"
