# THUNDERDOME :: td-service — an unauthenticated Redis instance.
# FOR ISOLATED PRACTICE ONLY.  Build context is the repo root.
FROM redis:7-alpine
COPY service_entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 6379
ENTRYPOINT ["/entrypoint.sh"]
