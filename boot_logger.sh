#!/bin/bash
set -e

PROJECT_DIR="/opt/fresher_project"
PYTHON="$PROJECT_DIR/venv/bin/python"
REPORT_JSON="$PROJECT_DIR/sys_report.json"
REPORT_HTML="$PROJECT_DIR/www/report.html"
LOG_FILE="/var/log/boot-logger.log"

echo "$(date -u): boot-logger service started" >> "$LOG_FILE"

# Generate the system report using the project virtual environment.
"$PYTHON" "$PROJECT_DIR/sys_report.py" --output "$REPORT_JSON"

# Preserve the existing delay.
sleep 60

# Generate a unified HTML report containing text logs and JSON data.
generate_html_report() {
    {
        cat <<HTML
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Fresher Project Boot Report</title>
</head>
<body>
    <h1>Fresher Project System Report</h1>
    <p>Generated: $(date -u)</p>

    <h2>Boot Logger Text Log</h2>
    <pre>
HTML

        tail -n 100 "$LOG_FILE" 2>/dev/null || true

        cat <<HTML
    </pre>

    <h2>System Snapshot (JSON)</h2>
    <pre>
HTML

        cat "$REPORT_JSON"

        cat <<HTML
    </pre>
</body>
</html>
HTML
    } > "$REPORT_HTML"
}

generate_html_report

echo "$(date -u): boot-logger service completed" >> "$LOG_FILE"
