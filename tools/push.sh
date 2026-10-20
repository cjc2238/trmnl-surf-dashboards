#!/usr/bin/env bash
# Send a payload to your Surf Call plugin's webhook.
#
#   export TRMNL_WEBHOOK_URL="https://trmnl.com/api/custom_plugins/<your-uuid>"
#   ./tools/push.sh plugins/surf-call/examples/midlength-progression.json
#
# Keep the URL out of git: anyone who has it can change your screen.
# Rate limit: 12 pushes/hour (30 on TRMNL+). A push may not redraw the screen
# right away -- see "Gotchas" in the README.
set -euo pipefail

: "${TRMNL_WEBHOOK_URL:?Set TRMNL_WEBHOOK_URL to the Webhook URL of your Surf Call plugin}"
payload="${1:?Usage: $0 payload.json}"

dir="$(cd "$(dirname "$0")" && pwd)"
python3 "$dir/validate_payload.py" "$payload"

curl -sS -X POST \
  -H "Content-Type: application/json" \
  --data @"$payload" \
  "$TRMNL_WEBHOOK_URL"
echo
