#!/usr/bin/env python3
"""THUNDERDOME :: td-web — a deliberately vulnerable "network tools" web box.

FOR ISOLATED PRACTICE ONLY. This app contains an intentional command-injection
vulnerability. Never run it on a machine reachable from an untrusted network.
"""
import subprocess
from flask import Flask, request, Response

app = Flask(__name__)

PAGE = """<!doctype html><meta charset=utf-8><title>NetTools</title>
<style>body{font-family:system-ui;max-width:640px;margin:40px auto;color:#eee;background:#111}
input,button{padding:6px;font-size:1rem}pre{background:#000;padding:10px;overflow:auto}</style>
<h2>NetTools &mdash; connectivity check</h2>
<form action="/ping"><input name="host" value="127.0.0.1" size=30>
<button>Ping</button></form>
<p>Internal admin utility. Pings a host and shows the result.</p>"""


@app.get("/")
def index():
    return PAGE


@app.get("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    # VULNERABILITY (by design): the user-controlled `host` is concatenated
    # straight into a shell command. This is the intended command-injection
    # foothold, e.g.  /ping?host=127.0.0.1;id  or  ;cat /home/td/user.txt
    out = subprocess.run("ping -c 1 " + host, shell=True,
                         capture_output=True, text=True, timeout=10)
    body = PAGE + "<hr><pre>" + (out.stdout or "") + (out.stderr or "") + "</pre>"
    return Response(body, mimetype="text/html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
