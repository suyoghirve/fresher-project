#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def get_cpu_load():
    """Return 1-, 5-, and 15-minute load averages."""
    try:
        load1, load5, load15 = os.getloadavg()

        return {
            "load_1min": load1,
            "load_5min": load5,
            "load_15min": load15
        }
    except (OSError, AttributeError) as exc:
        return {"error": str(exc)}


def get_memory():
    """Read memory statistics from /proc/meminfo."""
    try:
        meminfo = {}

        with Path("/proc/meminfo").open(encoding="utf-8") as file:
            for line in file:
                key, value = line.split(":", 1)
                meminfo[key] = int(value.strip().split()[0])

        total = meminfo["MemTotal"]
        available = meminfo["MemAvailable"]
        used = total - available

        return {
            "total_kb": total,
            "used_kb": used,
            "available_kb": available
        }

    except (OSError, KeyError, ValueError) as exc:
        return {"error": str(exc)}


def get_disk():
    """Return root filesystem usage in bytes."""
    try:
        usage = shutil.disk_usage("/")

        return {
            "total_bytes": usage.total,
            "used_bytes": usage.used,
            "free_bytes": usage.free,
            "used_percent": round(
                usage.used / usage.total * 100, 2
            ) if usage.total else 0
        }

    except OSError as exc:
        return {"error": str(exc)}


def get_top_service_errors():
    """Count error-priority journal lines from the current boot."""
    try:
        result = subprocess.run(
            [
                "journalctl",
                "-b",
                "-p", "err",
                "-n", "10000",
                "--no-pager",
                "-o", "cat"
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=30
        )

        if result.returncode != 0:
            return {
                "count": None,
                "error": result.stderr.strip()
                or f"journalctl exited with code {result.returncode}"
            }

        count = sum(
            1 for line in result.stdout.splitlines()
            if line.strip()
        )

        return {
            "count": count,
            "scope": "current_boot",
            "priority": "err",
            "limit": 10000
        }

    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "count": None,
            "error": str(exc)
        }


def build_report():
    """Collect all metrics into one report."""
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "hostname": os.uname().nodename,
        "cpu": get_cpu_load(),
        "memory": get_memory(),
        "disk": get_disk(),
        "journal_errors": get_top_service_errors()
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Linux system health report in JSON."
    )

    parser.add_argument(
        "-o",
        "--output",
        default="/opt/fresher_project/sys_report.json",
        help="Output JSON file path"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print the JSON report to stdout"
    )

    args = parser.parse_args()
    report = build_report()
    formatted_json = json.dumps(report, indent=2)

    output_path = Path(args.output).expanduser()

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", encoding="utf-8") as file:
            file.write(formatted_json + "\n")

    except OSError as exc:
        print(
            f"ERROR: Cannot write report to {output_path}: {exc}",
            file=sys.stderr
        )
        return 1

    if args.verbose:
        print(formatted_json)
    else:
        print(f"System report written to: {output_path}")

    if report["journal_errors"].get("count") is None:
        print(
            "WARNING: Could not collect journal errors: "
            + report["journal_errors"].get("error", "Unknown error"),
            file=sys.stderr
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
