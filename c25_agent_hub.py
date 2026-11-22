#!/usr/bin/env python3
import datetime, json, os, subprocess, sys
from pathos.multiprocessing import ProcessingPool as Pool

OLLAMA_URL = "http://127.0.0"
MODEL = "qwen2.5-coder:3b"
MAX_WORKERS = 5
OUT_DIR = os.path.expanduser("~/c25_reports")
os.makedirs(OUT_DIR, exist_ok=True)

AGENT_ROSTER = {
    "neo": "System architect & master coordinator",
    "repo_auditor": "Scans git status, missing modules, and broken remotes",
    "termux_fixer": "Diagnoses Android/Termux paths, permissions, and storage links",
    "obsidian_indexer": "Finds and links markdown notes across vaults",
    "git_syncer": "Handles commits, branches, and GitHub push/pull logic",
    "code_surgeon": "Refactors and debugs Python/Bash scripts",
    "security_warden": "Checks SSH keys, tokens, and exposed secrets",
    "deploy_router": "Prepares Vercel, tunnel, or local service deployments",
    "bloat_cleaner": "Identifies duplicate archives and safe cleanup targets",
    "manifest_reader": "Parses JSON audit logs and build manifests",
    "api_bridge": "Connects local endpoints, webhooks, and Ollama APIs",
    "tunnel_runner": "Manages Pinggy/SSH tunnels and port forwarding",
    "env_doctor": "Verifies Python, Node, and package dependencies",
    "log_detective": "Reads crash logs and extracts root causes",
    "test_runner": "Writes quick sanity checks and validation commands",
    "doc_writer": "Generates concise READMEs and runbooks",
    "schema_mapper": "Designs JSON/data structures between modules",
    "shell_optimizer": "Rewrites slow find/grep pipelines into fast one-liners",
    "backup_guard": "Verifies archive integrity before moving files",
    "dependency_mapper": "Traces imports and cross-repo links",
    "task_decomposer": "Breaks big goals into atomic shell steps",
    "port_watcher": "Checks active localhost ports and background daemons",
    "prompt_tuner": "Refines system prompts for local models",
    "release_packer": "Bundles scripts for clean distribution",
    "recovery_specialist": "Locates lost files across backups and quarantines",
}

def anchor_top():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def run_cmd(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=15).stdout.strip()
    except Exception:
        return ""

def toast(msg):
    subprocess.Popen(["termux-toast", "-g", "top", msg])

def get_anchored_paste_box():
    if "--auto-clip" in sys.argv:
        clip = run_cmd(["termux-clipboard-get"])
        if clip:
            toast("📷 QR Triggered: Synced Clipboard!")
            return clip
    anchor_top()
    print("=" * 54)
    print("📋 C25 PASTE BOX (Anchored Top | Termux-API Synced)")
    print("=" * 54)
    print("[Enter] Grab Android Clipboard | [d] Native Popup")
    print("Or paste directly below & press Ctrl+D:")
    print("-" * 54)
    first_line = sys.stdin.readline()
    if first_line == "\n":
        clip = run_cmd(["termux-clipboard-get"])
        if clip:
            toast("📋 Synced from Android Clipboard!")
            print(f"✅ Grabbed {len(clip)} chars from clipboard.")
            return clip
        print("⚠️ Clipboard empty. Paste below & press Ctrl+D:")
        return sys.stdin.read().strip()
    elif first_line.strip().lower() == "d":
        raw = run_cmd(["termux-dialog", "text", "-m", "-t", "C25 Qwen Paste Box"])
        try:
            return json.loads(raw).get("text", "").strip()
        except Exception:
            return ""
    try:
        return (first_line + sys.stdin.read()).strip()
    except KeyboardInterrupt:
        return ""

def ask_ollama(prompt, system="", json_mode=False):
    payload = {"model": MODEL, "prompt": prompt, "system": system, "stream": False}
    if json_mode:
        payload["format"] = "json"
    requests = _get_requests()
    requests = _get_requests()
    resp = requests.post(OLLAMA_URL, json=payload, timeout=180)
    resp.raise_for_status()
    return resp.json().get("response", "").strip()

def delegate_tasks(user_paste):
    roster_text = "\n".join([f"- {k}: {v}" for k, v in AGENT_ROSTER.items()])
    sys_p = (
        "You are Neo, the C25 master router. Pick the 5 best agents from the roster "
        "to solve the user's pasted input. Return ONLY valid JSON with a 'tasks' list "
        "of up to 5 items. Each item must have: 'agent' (exact key), 'task', 'command_hint'."
    )
    raw = ask_ollama(f"ROSTER:\n{roster_text}\n\nINPUT:\n{user_paste}", system=sys_p, json_mode=True)
    return json.loads(raw).get("tasks", [])[:MAX_WORKERS]

def run_single_agent(item):
    agent = item.get("agent", "worker")
    role = AGENT_ROSTER.get(agent, "Specialist agent")
    task = item.get("task", "")
    hint = item.get("command_hint", "")
    sys_msg = f"You are agent '{agent}' ({role}) in Termux. Be concise and give exact commands."
    try:
        out = ask_ollama(f"Task: {task}\nHint: {hint}\nOutput:", system=sys_msg)
        return f"\n🤖 [{agent.upper()}] — {task}\n{'-'*50}\n{out}\n"
    except Exception as e:
        return f"\n❌ [{agent.upper()}] Error: {e}\n"

def pop_clickable_txt_alert(txt_path, summary):
    subprocess.run(["termux-clipboard-set", txt_path], check=False)
    toast(f"✅ Saved {os.path.basename(txt_path)}")
    open_act = f"termux-open '{txt_path}'"
    subprocess.run([
        "termux-notification", "--id", "c25_agent_report",
        "--title", "⚡ C25 5-Agent Report Ready (.txt)",
        "--content", f"Tap to open: {os.path.basename(txt_path)} | {summary}",
        "--action", open_act, "--button1", "Open .txt", "--button1-action", open_act,
        "--button2", "Copy Text", "--button2-action", f"cat '{txt_path}' | termux-clipboard-set",
        "--priority", "high"
    ], check=False)

def main():
    pasted = get_anchored_paste_box()
    if not pasted:
        toast("⚠️ Nothing pasted.")
        return
    toast("🧠 Qwen delegating 5 agents...")
    tasks = delegate_tasks(pasted)
    if not tasks:
        print("⚠️ Qwen returned no tasks.")
        return
    anchor_top()
    print("=" * 54 + "\n📌 QWEN SUGGESTED 5-AGENT DELEGATION PLAN\n" + "=" * 54)
    for i, t in enumerate(tasks, 1):
        print(f"  {i}. [{t.get('agent')}] -> {t.get('task')}")
    if input("\n🚀 Run these 5 agents via pathos? [y/N]: ").strip().lower() != "y":
        toast("🛑 Cancelled")
        return
    toast("⚡ Dispatching 5 pathos agents...")
    with Pool(nodes=MAX_WORKERS) as pool:
        results = pool.map(run_single_agent, tasks)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_path = os.path.join(OUT_DIR, f"c25_report_{ts}.txt")
    full_report = f"C25 5-AGENT REPORT ({ts})\n{'='*54}\nPROMPT:\n{pasted}\n{'='*54}\n" + "".join(results)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(full_report)
    print(full_report)
    pop_clickable_txt_alert(txt_path, f"{len(tasks)} agents completed.")

if __name__ == "__main__":
    main()

_requests = None


def _get_requests():
    global _requests
    if _requests is None:
        import requests as req

        _requests = req
    return _requests


def fetch_json(url: str, timeout: float = 10.0) -> dict:
    requests = _get_requests()
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def send_payload(endpoint: str, payload: dict, timeout: float = 10.0) -> int:
    requests = _get_requests()
    resp = requests.post(endpoint, json=payload, timeout=timeout)
    return resp.status_code
