#!/usr/bin/env python3
"""THUNDERDOME grader — submit the flags you capture, track kill-chain progress.

  python3 grade.py THD{...} [THD{...} ...]   # submit one or more flags
  python3 grade.py                           # just show progress

Flags are verified by SHA-256, so this file does not reveal them.
"""
import sys, hashlib, json, os

STAGES = [
    ("web-foothold",  "Command injection on td-web  ->  user flag",
     "29659131f90eeb21c583a97b282cfe1e41c3e8996ab8015cfb7ee1ac79f9f599"),
    ("web-root",      "Privilege escalation on td-web  ->  root flag",
     "500fbff89a6d72bbaceee1e19930bb1a08984085f73f2e66c8ce0f2b966f2006"),
    ("service-redis", "Unauthenticated Redis on td-service  ->  flag",
     "928e80cf1d0d05444fe05dd15834aacae5e513c4c7bf7290934b29b22e338093"),
]
STATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".progress.json")


def load():
    try:
        return set(json.load(open(STATE)))
    except Exception:
        return set()


def save(s):
    try:
        json.dump(sorted(s), open(STATE, "w"))
    except Exception:
        pass


def main():
    done = load()
    for flag in sys.argv[1:]:
        h = hashlib.sha256(flag.strip().encode()).hexdigest()
        hit = next((k for k, _, hh in STAGES if hh == h), None)
        if hit and hit in done:
            print(f"[=] {flag}  already captured ({hit})")
        elif hit:
            done.add(hit)
            print(f"[+] {flag}  CORRECT  ->  {hit}")
        else:
            print(f"[-] {flag}  not a THUNDERDOME flag")
    save(done)
    print("\n=== THUNDERDOME progress ===")
    for k, desc, _ in STAGES:
        print(f"  [{'x' if k in done else ' '}] {k:14} {desc}")
    cleared = len(done) == len(STAGES)
    print(f"  {len(done)}/{len(STAGES)} captured" +
          ("   ===  RANGE CLEARED  ===" if cleared else ""))
    if cleared:
        print("\n  Ready for more? The Advanced Pack (Active Directory kill chain,"
              "\n  chained privesc, custom-exploit boxes) is on the Warboy Patreon.")


if __name__ == "__main__":
    main()
