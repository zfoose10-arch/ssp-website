#!/usr/bin/env bash
# Deploy the site to Hostinger over rsync/SSH (key auth).
# Always dry-runs first and requires explicit confirmation, because
# --delete makes the remote mirror the local site exactly.
set -euo pipefail

HOST="217.196.54.69"
PORT="65002"
USER="u619638832"
REMOTE_DIR="/home/u619638832/domains/summitspringpartners.com/public_html"

# Sync from the repo root regardless of where the script is invoked.
LOCAL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

EXCLUDES=(
  --include='/.htaccess'
  --exclude='/copy/'
  --exclude='/scripts/'
  --exclude='/.git/'
  --exclude='/.gitignore'
  --exclude='/.claude/'
  --exclude='/DEPLOY.md'
  --exclude='README*'
  --exclude='.DS_Store'
)

RSYNC_OPTS=(-rlptvz --delete -e "ssh -p $PORT")

echo "=== Dry run: what the deploy WOULD do ==="
rsync "${RSYNC_OPTS[@]}" --dry-run --itemize-changes "${EXCLUDES[@]}" \
  "$LOCAL_DIR/" "$USER@$HOST:$REMOTE_DIR/"
echo
echo "Lines starting with '*deleting' will be REMOVED from the server."
echo "Other listed files will be uploaded/updated."
echo

read -r -p "Run the real deploy? Type 'yes' to proceed: " REPLY
if [[ "$REPLY" != "yes" ]]; then
  echo "Aborted. Nothing was changed on the server."
  exit 1
fi

echo
echo "=== Deploying ==="
rsync "${RSYNC_OPTS[@]}" "${EXCLUDES[@]}" \
  "$LOCAL_DIR/" "$USER@$HOST:$REMOTE_DIR/"
echo
echo "Deploy complete: https://summitspringpartners.com"
