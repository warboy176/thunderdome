#!/bin/sh
set -e
# Place the flags inside the box. They are base64-encoded here only so a repo
# clone doesn't spoil the capture — the point is to reach them via the kill chain.
echo 'VEhEe3czYl9jMG1tNG5kXzFuajNjdDEwbn0=' | base64 -d > /home/td/user.txt
chown td:td /home/td/user.txt && chmod 644 /home/td/user.txt
echo 'VEhEe3IwMHRfdjE0X3N1ZDBfZ3RmMGIxbnN9' | base64 -d > /root/root.txt
chmod 600 /root/root.txt

# Serve the vulnerable app AS 'td' so the command-injection foothold lands as a
# low-priv user (td) — root comes from the privesc step, not for free.
cd /app
exec su td -c "python3 /app/app.py"
