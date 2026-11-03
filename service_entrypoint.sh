#!/bin/sh
# Seed the flag a couple of seconds after Redis comes up, then stay foreground.
( sleep 2
  FLAG=$(echo 'VEhEe3IzZDFzX3VuYXV0aF8zeHAwc3VyM30=' | base64 -d)
  redis-cli set thunderdome:flag "$FLAG" >/dev/null 2>&1
  redis-cli set note "No auth on this Redis. 'get thunderdome:flag' — on a real box an attacker would write an SSH key / cron to turn this into RCE." >/dev/null 2>&1
) &
# Intentional misconfiguration: protected-mode off, no password = unauthenticated exposure.
exec redis-server --protected-mode no --save ""
