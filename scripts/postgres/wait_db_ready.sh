#!/usr/bin/env bash

set -ex

echo wait_db_ready... >&2

for i in {0..30}; do
    pg_isready >/dev/null 2>&2 || (sleep 1; continue)
    echo Running! >&2
    exit 0
done
echo Timeout: PG failed to start in 30 seconds >&2
exit 255

