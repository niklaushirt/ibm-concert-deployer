#!/usr/bin/env bash

set -uo pipefail

# Format: "namespace|resource type|resource name"
# Leave namespace empty for cluster-scoped resources.
RESOURCES=(
  # "ibm-aiops|deployment|example-deployment"
  # "ibm-aiops|example.example.com|example-name"
  # "|namespace|example-namespace"
)


if [[ -n "${KUBE_CLI:-}" ]]; then
  if ! command -v "${KUBE_CLI}" >/dev/null 2>&1; then
    echo "Error: KUBE_CLI does not identify an installed command: ${KUBE_CLI}" >&2
    exit 1
  fi
elif command -v oc >/dev/null 2>&1; then
  KUBE_CLI="oc"
elif command -v kubectl >/dev/null 2>&1; then
  KUBE_CLI="kubectl"
else
  echo "Error: neither oc nor kubectl is installed." >&2
  exit 1
fi

if ((${#RESOURCES[@]} == 0)); then
  echo "No resources configured. Add entries to the RESOURCES array." >&2
  exit 1
fi

failures=0

for entry in "${RESOURCES[@]}"; do
  IFS='|' read -r namespace resource_type resource_name extra <<<"${entry}"

  if [[ -n "${extra:-}" || -z "${resource_type:-}" || -z "${resource_name:-}" ]]; then
    echo "Invalid resource entry: ${entry}" >&2
    echo 'Expected: "namespace|resource type|resource name"' >&2
    failures=$((failures + 1))
    continue
  fi

  namespace_args=()
  resource_label="${resource_type}/${resource_name}"
  if [[ -n "${namespace}" ]]; then
    namespace_args=(-n "${namespace}")
    resource_label="${resource_label} in namespace ${namespace}"
  fi

  if ! "${KUBE_CLI}" get "${resource_type}" "${resource_name}" "${namespace_args[@]}" >/dev/null 2>&1; then
    echo "Skipping ${resource_label}: not found."
    continue
  fi

  echo "Deleting ${resource_label}..."
  if ! "${KUBE_CLI}" delete "${resource_type}" "${resource_name}" \
    "${namespace_args[@]}" --ignore-not-found --wait=false; then
    echo "Warning: delete request failed for ${resource_label}." >&2
    failures=$((failures + 1))
  fi

  if "${KUBE_CLI}" get "${resource_type}" "${resource_name}" "${namespace_args[@]}" >/dev/null 2>&1; then
    echo "Removing finalizers from ${resource_label}..."
    if ! "${KUBE_CLI}" patch "${resource_type}" "${resource_name}" \
      "${namespace_args[@]}" --type=merge \
      --patch '{"metadata":{"finalizers":null}}'; then
      if "${KUBE_CLI}" get "${resource_type}" "${resource_name}" "${namespace_args[@]}" >/dev/null 2>&1; then
        echo "Warning: could not remove finalizers from ${resource_label}." >&2
        failures=$((failures + 1))
      fi
    fi
  fi

  if ! "${KUBE_CLI}" wait --for=delete "${resource_type}/${resource_name}" \
    "${namespace_args[@]}" --timeout=60s >/dev/null 2>&1; then
    echo "Warning: ${resource_label} still exists after 60 seconds." >&2
    failures=$((failures + 1))
  else
    echo "Deleted ${resource_label}."
  fi
done

if ((failures > 0)); then
  echo "Cleanup finished with ${failures} error(s)." >&2
  exit 1
fi

echo "Cleanup completed successfully."
