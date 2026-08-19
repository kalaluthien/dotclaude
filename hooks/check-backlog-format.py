#!/usr/bin/env python3
"""Retired 2026-08-19: the backlog grammar check moved to the board server.

A ticket is now filed, changed and closed through the board server's doors,
which check a request against the ticket contract *before* the write
(`~/workspace/board/docs/data-ticket-contract.md`), so an after-the-fact
check on a file has no job. A row still standing in a pool file is edited
without this check until its pool migrates, and the migration re-checks
every row at the filing door (`POST /api/tickets?validate=1`).

This stub stays only for live sessions that captured the old hook
registration at startup; it accepts everything. Delete it with the last
pool `backlog.md`.
"""

import sys

if len(sys.argv) == 1 and not sys.stdin.isatty():
    try:
        sys.stdin.read()
    except OSError:
        pass
sys.exit(0)
