#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="${ROOT_DIR}/docs"
ENV_FILE="${ROOT_DIR}/.env"
ENV_EXAMPLE_FILE="${ROOT_DIR}/.env.example"
VENV_DIR="${ROOT_DIR}/.venv"

FORCE_ENV=0
SKIP_DOCS=0
SKIP_PYTHON=0

usage() {
  cat <<'EOF'
Usage: ./setup.sh [options]

Bootstrap AutoPOM-Agent quickly:
  - creates .venv (if missing)
  - installs Python dependencies
  - installs docs dependencies
  - creates/updates .env with predefined defaults

Options:
  --force-env     Overwrite .env with predefined values
  --skip-python   Skip Python virtualenv and pip install
  --skip-docs     Skip docs npm install
  -h, --help      Show this help message
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force-env)
      FORCE_ENV=1
      shift
      ;;
    --skip-docs)
      SKIP_DOCS=1
      shift
      ;;
    --skip-python)
      SKIP_PYTHON=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      usage
      exit 1
      ;;
  esac
done

ensure_key() {
  local key="$1"
  local value="$2"
  if ! grep -Eq "^${key}=" "${ENV_FILE}"; then
    echo "${key}=${value}" >> "${ENV_FILE}"
  fi
}

bootstrap_env() {
  echo "Configuring .env..."

  if [[ "${FORCE_ENV}" -eq 1 ]]; then
    cat > "${ENV_FILE}" <<'EOF'
AUTOPOM_USERNAME=demo_user
AUTOPOM_PASSWORD=demo_password
AUTOPOM_BASE_URL=https://example.com
DOCS_URL=https://vinipx.github.io
DOCS_BASE_URL=/AUTOPOM/
EOF
    return
  fi

  if [[ ! -f "${ENV_FILE}" ]]; then
    if [[ -f "${ENV_EXAMPLE_FILE}" ]]; then
      cp "${ENV_EXAMPLE_FILE}" "${ENV_FILE}"
    else
      : > "${ENV_FILE}"
    fi
  fi

  ensure_key "AUTOPOM_USERNAME" "demo_user"
  ensure_key "AUTOPOM_PASSWORD" "demo_password"
  ensure_key "AUTOPOM_BASE_URL" "https://example.com"
  ensure_key "DOCS_URL" "https://vinipx.github.io"
  ensure_key "DOCS_BASE_URL" "/AUTOPOM/"
}

bootstrap_python() {
  if [[ "${SKIP_PYTHON}" -eq 1 ]]; then
    echo "Skipping Python bootstrap (--skip-python)."
    return
  fi

  if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: python3 not found in PATH."
    exit 1
  fi

  echo "Bootstrapping Python environment..."
  if [[ ! -d "${VENV_DIR}" ]]; then
    python3 -m venv "${VENV_DIR}"
  fi

  # shellcheck disable=SC1091
  source "${VENV_DIR}/bin/activate"
  python -m pip install --upgrade pip setuptools wheel
  python -m pip install -e ".[ai,browser,dev]"

  if command -v pre-commit >/dev/null 2>&1; then
    echo "Installing pre-commit hooks..."
    pre-commit install
  fi
}

bootstrap_docs() {
  if [[ "${SKIP_DOCS}" -eq 1 ]]; then
    echo "Skipping docs bootstrap (--skip-docs)."
    return
  fi

  if [[ ! -d "${DOCS_DIR}" ]]; then
    echo "Warning: docs directory not found at ${DOCS_DIR}; skipping docs setup."
    return
  fi

  if ! command -v npm >/dev/null 2>&1; then
    echo "Warning: npm not found in PATH; skipping docs setup."
    return
  fi

  echo "Installing docs dependencies..."
  (
    cd "${DOCS_DIR}"
    if [[ -f "package-lock.json" ]]; then
      npm ci
    else
      npm install
    fi
  )
}

main() {
  echo "Starting AutoPOM-Agent bootstrap..."
  bootstrap_env
  bootstrap_python
  bootstrap_docs

  cat <<EOF

Bootstrap complete.

Next steps:
  1) Activate environment:
     source "${VENV_DIR}/bin/activate"

  2) Code Quality:
     Pre-commit hooks are installed. They will run automatically on 'git commit'.
     Run manually: pre-commit run --all-files

  3) Run tests:
     PYTHONPATH=src python -m unittest discover -s tests -p "test_*_unittest.py" -v

  3) Run AutoPOM:
     PYTHONPATH=src python -m autopom.cli.main --base-url "\${AUTOPOM_BASE_URL:-https://example.com}" --output-dir output

  4) Start docs:
     ./docs.sh
EOF
}

main
