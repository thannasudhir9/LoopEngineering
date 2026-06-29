"""
AI Process Monitor — scans for Claude, Claude Code, Cursor, and other AI processes.
Runs every 5s in background, pushes updates to state store.
"""
import asyncio
import psutil
from . import state

AI_PROCESS_NAMES = {
    "claude": "Claude",
    "claude-code": "Claude Code",
    "cursor": "Cursor",
    "copilot": "GitHub Copilot",
    "continue": "Continue",
    "ollama": "Ollama",
    "lmstudio": "LM Studio",
    "aider": "Aider",
    "cody": "Cody",
}

CLAUDE_CODE_KEYWORDS = [
    "claude-code", "claude_code", "@anthropic", "anthropic-ai",
    "claude-sonnet", "claude-haiku", "claude-opus",
]
CURSOR_KEYWORDS = ["cursor", "cursorapp"]


def _classify_process(proc: psutil.Process) -> str | None:
    try:
        name = proc.name().lower()
        cmdline = " ".join(proc.cmdline()).lower()
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        return None

    for key, label in AI_PROCESS_NAMES.items():
        if key in name or key in cmdline:
            return label

    for kw in CLAUDE_CODE_KEYWORDS:
        if kw in cmdline:
            return "Claude Code"

    for kw in CURSOR_KEYWORDS:
        if kw in name or kw in cmdline:
            return "Cursor"

    return None


def scan_processes() -> list[dict]:
    found: list[dict] = []

    for proc in psutil.process_iter(["pid", "name", "status", "cpu_percent", "memory_info"]):
        label = _classify_process(proc)
        if not label:
            continue
        try:
            mem_mb = round(proc.memory_info().rss / 1024 / 1024, 1)
            cpu = proc.cpu_percent(interval=None)
            found.append({
                "pid": proc.pid,
                "label": label,
                "name": proc.name(),
                "status": proc.status(),
                "cpu_pct": cpu,
                "mem_mb": mem_mb,
            })
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue

    # Keep highest-memory entry per label
    by_label: dict[str, dict] = {}
    for p in found:
        lbl = p["label"]
        if lbl not in by_label or p["mem_mb"] > by_label[lbl]["mem_mb"]:
            by_label[lbl] = p

    return list(by_label.values())


async def monitor_loop(interval: float = 5.0):
    while True:
        try:
            procs = scan_processes()
            state.set_processes(procs)
        except Exception:
            pass
        await asyncio.sleep(interval)
