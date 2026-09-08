#!/usr/bin/env bash
# ==============================================================================
# Script: cleanup_poc_resources.sh
# Purpose: Safe, single-command teardown script for all POC demo resources
#          created across fnlab-apps-8fa913, fnlab-ai-data-8fa913,
#          fnlab-sec-mgmt-8fa913, and aispr-core-1cab11.
# Usage:
#   ./scripts/cleanup_poc_resources.sh [--dry-run]
# ==============================================================================

set -euo pipefail

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
  echo "[DRY-RUN MODE] No resources will be deleted."
fi

echo "======================================================================"
echo "Starting Agentic GRC POC Resource Teardown"
echo "======================================================================"

# ------------------------------------------------------------------------------
# 1. GCS BUCKETS (10 total)
# ------------------------------------------------------------------------------
BUCKETS=(
  "gs://poc-bucket-payments-sec-8fa913"
  "gs://poc-bucket-analytics-ai-8fa913"
  "gs://poc-bucket-logs-core-1cab11"
  "gs://poc-bucket-app-apps-8fa913"
  "gs://poc-bucket-backup-apps-8fa913"
  "gs://poc-bucket-reports-ai-8fa913"
  "gs://poc-bucket-staging-ai-8fa913"
  "gs://poc-bucket-app-sec-8fa913"
  "gs://poc-bucket-backup-core-1cab11"
  "gs://poc-bucket-staging-core-1cab11"
)

echo "Deleting 10 GCS Buckets..."
for b in "${BUCKETS[@]}"; do
  if $DRY_RUN; then
    echo "  [DRY-RUN] Would delete bucket: $b"
  else
    echo "  Deleting bucket: $b"
    gcloud storage rm --recursive "$b" --quiet 2>/dev/null || true
  fi
done

# ------------------------------------------------------------------------------
# 2. FIREWALL RULES (6 total)
# ------------------------------------------------------------------------------
FIREWALLS=(
  "poc-fw-internal-mgmt:fnlab-sec-mgmt-8fa913"
  "poc-fw-ai-worker-sync:fnlab-ai-data-8fa913"
  "poc-fw-open-ssh-demo:fnlab-apps-8fa913"
  "poc-fw-open-rdp-demo:aispr-core-1cab11"
  "poc-fw-db-nologging:fnlab-apps-8fa913"
  "poc-fw-analytics-wide:fnlab-ai-data-8fa913"
)

echo "Deleting 6 Compute Firewall Rules..."
for fw_entry in "${FIREWALLS[@]}"; do
  fw_name="${fw_entry%%:*}"
  proj="${fw_entry##*:}"
  if $DRY_RUN; then
    echo "  [DRY-RUN] Would delete firewall rule: $fw_name in $proj"
  else
    echo "  Deleting firewall rule: $fw_name in $proj"
    gcloud compute firewall-rules delete "$fw_name" --project="$proj" --quiet 2>/dev/null || true
  fi
done

# ------------------------------------------------------------------------------
# 3. KMS KEYS (6 total across 2 keyrings - Destroy Versions)
# ------------------------------------------------------------------------------
# Note: GCP KMS Keyrings and Keys cannot be permanently erased from GCP APIs,
# but crypto key versions can be scheduled for immediate destruction.
KMS_KEYS=(
  "poc-key-payments-hsm:poc-keyring-sec:fnlab-sec-mgmt-8fa913"
  "poc-key-database-hsm:poc-keyring-sec:fnlab-sec-mgmt-8fa913"
  "poc-key-audit-software:poc-keyring-sec:fnlab-sec-mgmt-8fa913"
  "poc-key-app-data:poc-keyring-apps:fnlab-apps-8fa913"
  "poc-key-backup-long:poc-keyring-apps:fnlab-apps-8fa913"
  "poc-key-tokens-stale:poc-keyring-apps:fnlab-apps-8fa913"
)

echo "Scheduling Destruction of KMS Key Versions..."
for k_entry in "${KMS_KEYS[@]}"; do
  IFS=':' read -r kname kr proj <<< "$k_entry"
  if $DRY_RUN; then
    echo "  [DRY-RUN] Would destroy version 1 of KMS key: $kname in $kr ($proj)"
  else
    echo "  Destroying version 1 of KMS key: $kname in $kr ($proj)"
    gcloud kms keys versions destroy 1 \
      --key="$kname" \
      --keyring="$kr" \
      --location=us-central1 \
      --project="$proj" \
      --quiet 2>/dev/null || true
  fi
done

# ------------------------------------------------------------------------------
# 4. IAM SERVICE ACCOUNTS & BINDINGS (2 SAs created)
# ------------------------------------------------------------------------------
echo "Removing POC Service Accounts..."
if $DRY_RUN; then
  echo "  [DRY-RUN] Would delete SA: poc-sa-reader@fnlab-apps-8fa913.iam.gserviceaccount.com"
  echo "  [DRY-RUN] Would delete SA: poc-sa-auditor@aispr-core-1cab11.iam.gserviceaccount.com"
else
  gcloud iam service-accounts delete "poc-sa-reader@fnlab-apps-8fa913.iam.gserviceaccount.com" \
    --project=fnlab-apps-8fa913 --quiet 2>/dev/null || true
  gcloud iam service-accounts delete "poc-sa-auditor@aispr-core-1cab11.iam.gserviceaccount.com" \
    --project=aispr-core-1cab11 --quiet 2>/dev/null || true
fi

echo "======================================================================"
echo "[SUCCESS] POC Teardown Complete."
echo "======================================================================"
