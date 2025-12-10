#!/bin/bash
# Sovereign Architect Agent - shell wrapper

GOAL="$*"
if [[ -z "$GOAL" ]]; then
  echo "Usage: agent_architect.sh \"your goal here\""
  exit 1
fi

# Run from repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

python "$REPO_ROOT/agents/architect_planner.py" "$GOAL"
