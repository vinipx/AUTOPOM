#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="${ROOT_DIR}/docs"
HOST="${HOST:-localhost}"
PORT="${PORT:-3000}"

if [[ ! -d "${DOCS_DIR}" ]]; then
  echo "Error: docs directory not found at ${DOCS_DIR}"
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "Error: npm is required but was not found in PATH."
  exit 1
fi

cd "${DOCS_DIR}"

if [[ ! -d "node_modules" ]]; then
  echo "Installing documentation dependencies..."
  if [[ -f "package-lock.json" ]]; then
    npm ci
  else
    npm install
  fi
else
  echo "Dependencies already installed (node_modules found)."
fi

echo "Building documentation site..."
npm run build

echo "Serving documentation at http://${HOST}:${PORT}"
npm run serve -- --host "${HOST}" --port "${PORT}"
