#!/bin/bash
# Run a command gently: background priority, 2 threads, at most 80 extra processes, time limit.
# Usage: limit.sh SECONDS command...
secs=$1; shift
ulimit -u $(( $(ps -U "$(id -u)" | wc -l) + 80 ))
export OMP_NUM_THREADS=2 VECLIB_MAXIMUM_THREADS=2 OPENBLAS_NUM_THREADS=2
exec perl -e 'alarm shift; exec @ARGV' "$secs" /usr/sbin/taskpolicy -b nice -n 19 "$@"
