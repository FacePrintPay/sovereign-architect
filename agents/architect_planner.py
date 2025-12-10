#!/usr/bin/env python3
import json, os, sys, uuid, datetime
from rich.console import Console
console = Console()

goal = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""

if not goal:
    console.print("[red]No goal provided[/red]")
    sys.exit(1)

plan_id = str(uuid.uuid4())[:8]
timestamp = datetime.datetime.now().isoformat()

plan = {
    "plan_id": plan_id,
    "goal": goal,
    "created_at": timestamp,
    "status": "planned",
    "steps": [
        {"step_id": 1, "title": "Market & Problem Validation", "objective": "Deep dive into pain points and TAM", "status": "pending"},
        {"step_id": 2, "title": "Product Architecture & Roadmap", "objective": "Define SovereignGTP tech stack & MVP", "status": "pending"},
        {"step_id": 3, "title": "Financial Model & Valuation", "objective": "Build 5-year P&L, cap table, $XM pre-money case", "status": "pending"},
        {"step_id": 4, "title": "Competitive Moat Analysis", "objective": "Why we win vs OpenAI/Anthropic/etc", "status": "pending"},
        {"step_id": 5, "title": "Regulatory & Compliance Framing", "objective": "GDPR, AI Act, data sovereignty strategy", "status": "pending"},
        {"step_id": 6, "title": "Go-to-Market & Traction Plan", "objective": "First 10 design partners + revenue timeline", "status": "pending"},
        {"step_id": 7, "title": "Team & Advisors", "objective": "Core team + killer advisory board", "status": "pending"},
        {"step_id": 8, "title": "Deck Design (Banani-ready)", "objective": "10 perfect slides, Notion/Pitch/Gamma export", "status": "pending"},
        {"step_id": 9, "title": "Investor Targeting List", "objective": "Top 50 funds + warm intros", "status": "pending"},
        {"step_id": 10, "title": "Outreach Sequences", "objective": "Cold + warm email/copy + calendar links", "status": "pending"}
    ]
}

os.makedirs(os.path.expanduser("~/plans"), exist_ok=True)
plan_file = f"~/plans/plan_{plan_id}_{int(datetime.datetime.now().timestamp())}.json"
with open(os.path.expanduser(plan_file), "w") as f:
    json.dump(plan, f, indent=2)

console.print(f"[bold green]Plan created![/green] → {plan_file}")
console.print(f"[bold]Goal:[/bold] {goal}")
