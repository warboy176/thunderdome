# THUNDERDOME :: td-web — deliberately vulnerable "network tools" box.
# FOR ISOLATED PRACTICE ONLY.  Build context is the repo root.
FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends iputils-ping sudo gawk procps coreutils \
 && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash td \
 && pip install --no-cache-dir flask==3.0.3

# --- intentional misconfiguration (the privilege-escalation path) ---
# 'td' is allowed to run awk as root with no password. awk can spawn a shell
# (GTFOBins), so this is a root path once you have a foothold as td.
RUN echo 'td ALL=(root) NOPASSWD: /usr/bin/awk' > /etc/sudoers.d/td \
 && chmod 440 /etc/sudoers.d/td

COPY web_app.py /app/app.py
COPY web_entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8080
ENTRYPOINT ["/entrypoint.sh"]
