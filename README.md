# Fresher Project – Automated Linux System Reporting

A hands-on DevOps project built on **Amazon Linux 2023**, using Bash, Python, systemd, and Nginx to automate Linux system monitoring, boot logging, and HTML report generation.

---

## 1. Project Overview

The Fresher Project automates the collection of Linux system health information and generates a consolidated HTML report.

A Bash automation script invokes a Python system-reporting utility through a dedicated Python virtual environment. A systemd service and timer automate execution, while Nginx provides HTTP and HTTPS access to the generated report.

The project demonstrates practical DevOps skills involving:

- Linux system administration.
- Bash scripting and automation.
- Python system monitoring.
- Git and GitHub version control.
- Python virtual environments.
- systemd services and timers.
- Nginx web server configuration.
- SELinux permissions and security.
- Linux firewall management.

## 2. Architecture

The reporting workflow operates as follows:

```text
              systemd Timer
             (Every 15 Minutes)
                     |
                     v
           boot-logger.service
                     |
                     v
              boot_logger.sh
                     |
           +---------+----------+
           |                    |
           v                    v
       sys_report.py        Boot Logger
           |                /var/log/
           v                boot-logger.log
     sys_report.json             |
           |                    |
           +---------+----------+
                     |
                     v
           HTML Report Generator
                     |
                     v
              www/report.html
                     |
                     v
                   Nginx
                     |
               HTTP / HTTPS
                     |
                     v
                Web Browser
```

### Execution Workflow

1. The systemd timer triggers the `boot-logger.service`.
2. The service executes `boot_logger.sh` as the `svc_fresher` user.
3. The Bash script records the service start timestamp.
4. The Python utility collects Linux system information.
5. The system snapshot is written to a JSON file.
6. The script waits 60 seconds.
7. An HTML report is generated containing the latest 100 boot log entries and the JSON system snapshot.
8. The service records its completion timestamp.
9. Nginx serves the generated HTML report.

## 3. Project Features

### 3.1 Linux System Monitoring

The Python utility (`sys_report.py`) collects the following information:

| Metric | Collection Method |
|---|---|
| Hostname | Python `os.uname()` |
| Report timestamp | Python UTC datetime |
| CPU load averages | `os.getloadavg()` |
| Memory statistics | `/proc/meminfo` |
| Disk usage | Python `shutil.disk_usage()` |
| Journal errors | `journalctl` |

CPU monitoring includes:

- 1-minute load average.
- 5-minute load average.
- 15-minute load average.

Memory monitoring includes:

- Total memory.
- Used memory.
- Available memory.

Disk monitoring includes:

- Total root filesystem capacity.
- Used space.
- Available space.
- Utilization percentage.

Journal monitoring counts error-priority entries from the current boot, using a maximum collection limit of 10,000 entries.

The collected information is stored in JSON format.

### 3.2 Automated Boot Logging

The Bash script (`boot_logger.sh`) performs the reporting workflow.

Key functionality:

- Records service start and completion timestamps.
- Executes the Python reporting utility.
- Uses the dedicated Python virtual environment.
- Generates a consolidated HTML report.
- Includes the latest 100 boot logger entries.
- Includes the latest JSON system snapshot.

The script uses `set -e` to stop execution when a command fails.

### 3.3 Python Virtual Environment

The project uses a dedicated Python virtual environment:

```text
/opt/fresher_project/venv
```

Python executable:

```text
/opt/fresher_project/venv/bin/python
```

This isolates the project's Python environment from the system Python installation.

The reporting utility currently uses Python standard-library modules and does not require third-party packages.

### 3.4 systemd Automation

The project uses systemd to automate execution.

Service unit:

```text
/etc/systemd/system/boot-logger.service
```

Timer unit:

```text
/etc/systemd/system/boot-logger.timer
```

Configuration highlights:

- Dedicated service account: `svc_fresher`
- Service script: `boot_logger.sh`
- Execution interval: Every 15 minutes.
- Automated execution through a systemd timer.

### 3.5 HTML Reporting with Nginx

The generated HTML report is stored at:

```text
/opt/fresher_project/www/report.html
```

Nginx serves the report over HTTP and HTTPS.

The lab environment uses a self-signed HTTPS certificate.

---

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Amazon Linux 2023 | Operating system |
| Bash | Automation and boot logging |
| Python 3 | System information collection |
| Python Virtual Environment | Python environment isolation |
| systemd | Service and timer management |
| Nginx | HTTP and HTTPS hosting |
| Git | Version control |
| GitHub | Source code hosting |
| SELinux | Mandatory access control |
| firewalld | Firewall management |
| JSON | System report data |
| HTML | Web-based report presentation |

---

## 5. Project Structure

```text
/opt/fresher_project/
│
├── .gitignore
├── README.md
├── LICENSE
│
├── boot_logger.sh
├── sys_report.py
│
├── venv/                       # Python virtual environment
├── logs/                       # Runtime log directory
├── reports/                    # Generated reports
│
├── sys_report.json             # Generated system snapshot
│
└── www/
    └── report.html             # Generated HTML report
```

**Note:** The `venv/`, `logs/`, `reports/`, JSON output, and generated HTML report are runtime artifacts. They are excluded from Git through `.gitignore`.

The systemd unit files and Nginx configuration are maintained separately under their respective system configuration directories.

---

## 6. Prerequisites

The project was developed and tested in an Amazon Linux 2023 environment.

Required components:

- Amazon Linux 2023 or compatible Linux distribution.
- Python 3.
- Bash.
- systemd.
- Nginx.
- Git.
- firewalld.

The Python reporting utility uses standard-library modules, so no external Python packages are currently required.

---

## 7. Installation and Setup

### 7.1 Clone the Repository

```bash
git clone git@github.com:suyoghirve/fresher-project.git

cd fresher-project
```

### 7.2 Create a Python Virtual Environment

```bash
python3 -m venv /opt/fresher_project/venv
```

### 7.3 Configure Permissions

The reporting service uses a dedicated Linux account:

```text
svc_fresher
```

Ensure the service account has the necessary permissions to:

- Execute the Bash and Python scripts.
- Write the JSON report.
- Write the generated HTML report.
- Append entries to `/var/log/boot-logger.log`.

The deployment also requires the project to be available at:

```text
/opt/fresher_project
```

---

## 8. Manual Execution

### 8.1 Execute the Complete Reporting Pipeline

Run the Bash script as the service account:

```bash
runuser -u svc_fresher -- \
  /opt/fresher_project/boot_logger.sh
```

### 8.2 Execute Only the Python Reporting Utility

```bash
runuser -u svc_fresher -- \
  /opt/fresher_project/venv/bin/python \
  /opt/fresher_project/sys_report.py \
  --output /opt/fresher_project/sys_report.json
```

### 8.3 Display the JSON Report in the Terminal

```bash
runuser -u svc_fresher -- \
  /opt/fresher_project/venv/bin/python \
  /opt/fresher_project/sys_report.py \
  --verbose
```

### 8.4 Inspect the Generated JSON

```bash
cat /opt/fresher_project/sys_report.json
```

---

## 9. systemd Service and Timer Management

### Check Service Status

```bash
systemctl status boot-logger.service
```

### Check Timer Status

```bash
systemctl status boot-logger.timer
```

### Start the Service Manually

```bash
systemctl start boot-logger.service
```

### Enable the Timer at System Startup

```bash
systemctl enable --now boot-logger.timer
```

### Check Scheduled Execution

```bash
systemctl list-timers --all
```

### Inspect Service Logs

```bash
journalctl -u boot-logger.service -n 50 --no-pager
```

### Follow Service Logs in Real Time

```bash
journalctl -u boot-logger.service -f
```

---

## 10. Output Locations

| Output | Location |
|---|---|
| System snapshot JSON | `/opt/fresher_project/sys_report.json` |
| Generated HTML report | `/opt/fresher_project/www/report.html` |
| Boot logger text log | `/var/log/boot-logger.log` |
| Project log directory | `/opt/fresher_project/logs/` |
| Python virtual environment | `/opt/fresher_project/venv/` |

The HTML report contains:

1. Report generation timestamp.
2. Latest 100 lines of the boot logger text log.
3. Current Linux system snapshot in JSON format.

---

## 11. Accessing the HTML Report

### HTTP Access

```text
http://fresher-local:8080/report.html
```

### HTTPS Access

```text
https://fresher-local/report.html
```

The lab HTTPS endpoint uses a self-signed certificate.

For local testing:

```bash
curl -k https://localhost/report.html
```

The `-k` option disables TLS certificate verification. It is intended only for testing with the lab's self-signed certificate.

---

## 12. Security and Permissions

The project incorporates several Linux security practices.

### 12.1 Dedicated Service Account

The systemd service runs under:

```text
svc_fresher
```

This avoids running the application workflow directly as root.

### 12.2 SELinux

The Nginx report directory uses the SELinux file context:

```text
httpd_sys_content_t
```

Check SELinux status:

```bash
getenforce
```

### 12.3 Firewall

Check firewalld status:

```bash
systemctl is-active firewalld
```

List allowed firewall services:

```bash
firewall-cmd --list-services
```

HTTP and HTTPS access should be allowed according to the lab's network requirements.

### 12.4 Git Security

The repository's `.gitignore` excludes:

- Python virtual environments.
- Python cache files.
- Runtime logs.
- Generated reports.
- Local environment files.
- Private keys and certificates.
- Terraform state files.
- IDE-specific files.
- Temporary and backup files.

Never commit passwords, cloud credentials, SSH private keys, access tokens, or other sensitive information.

Generated system reports may contain infrastructure information. Do not expose sensitive production reports through a public repository or publicly accessible web server.

---

## 13. Troubleshooting

### Check the Python System Report

```bash
cat /opt/fresher_project/sys_report.json
```

### Check the Generated HTML Report

```bash
grep -nE 'Boot Logger Text Log|System Snapshot' \
  /opt/fresher_project/www/report.html
```

### Check HTTP Access

```bash
curl -I -H 'Host: fresher-local' \
  http://127.0.0.1:8080/report.html
```

### Check HTTPS Access

```bash
curl -k -I https://localhost/report.html
```

### Check systemd Execution

```bash
journalctl -u boot-logger.service -n 50 --no-pager
```

### Check Timer Execution

```bash
systemctl list-timers --all
```

---

## 14. Extending the Project

The project can be extended with additional DevOps capabilities.

Potential enhancements:

1. Add CPU utilization and additional system metrics.
2. Include network interface statistics.
3. Add filesystem monitoring for multiple mount points.
4. Improve HTML report formatting and visualizations.
5. Introduce configurable alert thresholds.
6. Integrate centralized monitoring and alerting.
7. Add Python unit tests.
8. Implement CI/CD automation using GitHub Actions.
9. Automate infrastructure deployment using Terraform.
10. Use Ansible for configuration management.

---

## 15. Learning Outcomes

This project demonstrates practical implementation of:

- Linux administration and troubleshooting.
- Bash scripting.
- Python automation.
- Linux system monitoring.
- systemd service and timer management.
- Nginx web server configuration.
- HTTP and HTTPS configuration.
- SELinux and firewalld management.
- Git branching and GitHub collaboration.
- Repository documentation and licensing.

---

## 16. Repository

**GitHub:** https://github.com/suyoghirve/fresher-project

---

## 17. License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.
