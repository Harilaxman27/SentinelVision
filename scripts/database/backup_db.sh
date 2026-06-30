#!/usr/bin/env bash
set -e
pg_dump -U sentinelvision -h localhost sentinelvision > backup.sql
