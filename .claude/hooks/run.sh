#!/bin/sh
# Launcher for the hooks in this folder: `sh .claude/hooks/run.sh <hook>.py [args]`.
#
# Picks the first interpreter that runs Python >= 3.9: $UAW_PYTHON, python3, python. Stock macOS
# only has python3 (3.9), many Linux images only python3, Windows (Git Bash) often only python;
# a Microsoft Store stub fails the version probe and is skipped. No interpreter -> one line on
# stderr and exit 0, so a hook never blocks a session. stdin (the hook payload) passes through.
here=$(dirname "$0")
script="$1"
shift
for py in "${UAW_PYTHON:-}" python3 python; do
  [ -n "$py" ] || continue
  command -v "$py" >/dev/null 2>&1 || continue
  if "$py" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' >/dev/null 2>&1; then
    UAW_PY="$py" exec "$py" "$here/$script" "$@"
  fi
done
echo "uaw hook $script: no Python >= 3.9 found (set UAW_PYTHON)" >&2
exit 0
