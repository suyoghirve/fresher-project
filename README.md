# Fresher Project — Automated System Reporting

## 1. Project Purpose

This project automates Linux system monitoring and boot logging on
Amazon Linux 2023.

A Bash script invokes a Python system-reporting program through a
dedicated Python virtual environment. The generated system snapshot
and boot log are combined into an HTML report served by Nginx.

## 2. Project Structure

/opt/fresher_project/
├── boot_logger.sh
├── boot_logger.sh.bak
├── sys_report.py
├── sys_report.json
├── venv/
├── logs/
├── reports/
└── www/
    └── report.html

## 3. Manual Execution

Run the complete reporting pipeline as the service user:

    runuser -u svc_fresher -- /opt/fresher_project/boot_logger.sh

Run only the Python system report:

    runuser -u svc_fresher -- \
      /opt/fresher_project/venv/bin/python \
      /opt/fresher_project/sys_report.py \
      --output /opt/fresher_project/sys_report.json

## 4. Python Virtual Environment

The project uses a dedicated virtual environment:

    /opt/fresher_project/venv

Python executable:

    /opt/fresher_project/venv/bin/python

This isolates project Python dependencies from the system Python.

## 5. Systemd Automation

Service unit:

    /etc/systemd/system/boot-logger.service

Timer unit:

    /etc/systemd/system/boot-logger.timer

The service runs as svc_fresher and executes boot_logger.sh.

The systemd timer triggers the service every 15 minutes.

Check service status:

    systemctl status boot-logger.service

Check timer status:

    systemctl status boot-logger.timer

Run the service manually:

    systemctl start boot-logger.service

Inspect service logs:

    journalctl -u boot-logger.service -n 50 --no-pager

The timer is enabled to start automatically when the system boots.

## 6. Output Locations

| Output | Location |
|---|---|
| System snapshot JSON | /opt/fresher_project/sys_report.json |
| HTML report | /opt/fresher_project/www/report.html |
| Boot logger text log | /var/log/boot-logger.log |
| Project log directory | /opt/fresher_project/logs/ |

The HTML report includes the latest 100 lines of the boot logger
text log and the current JSON system snapshot.

## 7. Report Access

HTTP:

    http://fresher-local:8080/report.html

HTTPS:

    https://fresher-local/report.html

The HTTPS lab endpoint uses a self-signed certificate. For local
testing with curl:

    curl -k https://localhost/report.html

## 8. Security and Permissions

The systemd service runs under the dedicated svc_fresher account.

The report directory uses the SELinux file context:

    httpd_sys_content_t

Verify SELinux mode:

    getenforce

Verify firewalld:

    systemctl is-active firewalld
    firewall-cmd --list-services

HTTP and HTTPS should be allowed by the firewall.

## 9. Extending the Project

To add new system metrics:

1. Update sys_report.py with the required metric collection logic.
2. Add the new metric to the generated JSON report.
3. Update boot_logger.sh or the HTML report generation logic if
   the new metric needs a dedicated presentation section.
4. Run the script manually as svc_fresher.
5. Verify the JSON and HTML output.
6. Test the systemd service and inspect its journal logs.

## 10. Troubleshooting

Check the Python report:

    cat /opt/fresher_project/sys_report.json

Check the HTML report:

    grep -nE 'Boot Logger Text Log|System Snapshot' \
      /opt/fresher_project/www/report.html

Check HTTP access:

    curl -I -H 'Host: fresher-local' \
      http://127.0.0.1:8080/report.html

Check HTTPS access:

    curl -k -I https://localhost/report.html

Check systemd execution:

    journalctl -u boot-logger.service -n 50 --no-pager
