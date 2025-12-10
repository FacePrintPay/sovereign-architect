#!/bin/bash
GOAL="$*"
if [[ -z "$GOAL" ]]; then
  echo "Usage: agent_architect.sh \"your goal here\""
  exit 1
fi

python ~/agents/architect_planner.py "$GOAL"
