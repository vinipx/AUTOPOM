#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
PYPROJECT_FILE="${ROOT_DIR}/pyproject.toml"
BASE_DEPS_MARKER="${VENV_DIR}/.autopom_base_deps_fingerprint"
BROWSER_DEPS_MARKER="${VENV_DIR}/.autopom_browser_deps_fingerprint"

info() {
  echo "[INFO] $*"
}

warn() {
  echo "[WARN] $*"
}

err() {
  echo "[ERROR] $*"
}

print_header() {
  echo "============================================================"
  echo " AUTOPOM Interactive Runner"
  echo "============================================================"
  echo
}

print_section() {
  echo
  echo "------------------------------------------------------------"
  echo " $1"
  echo "------------------------------------------------------------"
}

require_python() {
  if ! command -v python3 >/dev/null 2>&1; then
    err "python3 was not found in PATH."
    exit 1
  fi
}

ensure_venv() {
  if [[ ! -d "${VENV_DIR}" ]]; then
    info "Creating virtual environment at ${VENV_DIR} ..."
    python3 -m venv "${VENV_DIR}"
  fi
}

activate_venv() {
  # shellcheck disable=SC1091
  source "${VENV_DIR}/bin/activate"
}

prompt_default() {
  local prompt_text="$1"
  local default_value="$2"
  local result
  read -r -p "${prompt_text} (default -> ${default_value}): " result
  if [[ -z "${result}" ]]; then
    result="${default_value}"
  fi
  printf "%s" "${result}"
}

prompt_positive_int() {
  local prompt_text="$1"
  local default_value="$2"
  while true; do
    local value
    value="$(prompt_default "${prompt_text}" "${default_value}")"
    if [[ "${value}" =~ ^[0-9]+$ ]] && (( value > 0 )); then
      printf "%s" "${value}"
      return 0
    fi
    warn "Please provide a positive integer."
  done
}

prompt_url() {
  local default_value="$1"
  while true; do
    local value
    value="$(prompt_default "Base URL to crawl" "${default_value}")"
    if [[ "${value}" =~ ^https?://.+ ]]; then
      printf "%s" "${value}"
      return 0
    fi
    warn "Please provide a valid URL starting with http:// or https://"
  done
}

prompt_yes_no() {
  local prompt_text="$1"
  local default_answer="$2"
  local answer
  local suffix="y/N"
  if [[ "${default_answer}" == "y" ]]; then
    suffix="Y/n"
  fi
  read -r -p "${prompt_text} (${suffix}, default -> ${default_answer}): " answer
  answer="${answer:-${default_answer}}"
  [[ "${answer}" =~ ^[Yy]$ ]]
}

dependency_fingerprint() {
  local extras_tag="$1"
  python - "${PYPROJECT_FILE}" "${extras_tag}" <<'PY'
import hashlib
import sys
from pathlib import Path

pyproject_path = Path(sys.argv[1])
extras_tag = sys.argv[2]
content = pyproject_path.read_bytes() if pyproject_path.exists() else b""
digest = hashlib.sha256(content + b"::" + extras_tag.encode("utf-8")).hexdigest()
print(digest)
PY
}

marker_matches() {
  local marker_path="$1"
  local expected_value="$2"
  if [[ ! -f "${marker_path}" ]]; then
    return 1
  fi
  local current_value
  current_value="$(<"${marker_path}")"
  [[ "${current_value}" == "${expected_value}" ]]
}

write_marker() {
  local marker_path="$1"
  local value="$2"
  printf "%s" "${value}" > "${marker_path}"
}

playwright_python_ready() {
  python - <<'PY'
import importlib.util
import sys

sys.exit(0 if importlib.util.find_spec("playwright") else 1)
PY
}

playwright_chromium_ready() {
  python - <<'PY'
import os
import sys

try:
    from playwright.sync_api import sync_playwright
except Exception:
    sys.exit(1)

try:
    p = sync_playwright().start()
    executable = p.chromium.executable_path
    p.stop()
except Exception:
    sys.exit(1)

sys.exit(0 if executable and os.path.exists(executable) else 1)
PY
}

choose_from_list() {
  local prompt_text="$1"
  local default_index="$2"
  shift 2
  local options=("$@")
  local i
  if (( default_index < 1 || default_index > ${#options[@]} )); then
    err "Internal error: invalid default index for '${prompt_text}'."
    exit 1
  fi

  echo "${prompt_text}" >&2
  for i in "${!options[@]}"; do
    local marker=" "
    if (( i + 1 == default_index )); then
      marker="*"
    fi
    echo "  ${marker} $((i + 1))) ${options[i]}" >&2
  done
  echo "  default -> ${options[$((default_index - 1))]} (option ${default_index})" >&2

  while true; do
    local choice
    read -r -p "Select option number (default -> ${default_index}): " choice
    if [[ -z "${choice}" ]]; then
      choice="${default_index}"
    fi
    if [[ "${choice}" =~ ^[0-9]+$ ]] && (( choice >= 1 && choice <= ${#options[@]} )); then
      printf "%s" "${options[$((choice - 1))]}"
      return 0
    fi
    warn "Invalid selection. Choose a number between 1 and ${#options[@]}."
  done
}

install_base_dependencies_if_needed() {
  local expected_fingerprint
  expected_fingerprint="$(dependency_fingerprint "dev")"
  if marker_matches "${BASE_DEPS_MARKER}" "${expected_fingerprint}"; then
    info "Base Python dependencies already up to date. Skipping reinstall."
    return
  fi

  info "Installing/updating base Python dependencies (editable + dev extras)..."
  python -m pip install --upgrade pip setuptools wheel
  python -m pip install -e ".[dev]"
  write_marker "${BASE_DEPS_MARKER}" "${expected_fingerprint}"
}

ensure_playwright_ready() {
  local expected_fingerprint
  expected_fingerprint="$(dependency_fingerprint "browser")"

  if marker_matches "${BROWSER_DEPS_MARKER}" "${expected_fingerprint}" && playwright_python_ready; then
    info "Playwright Python dependency already up to date."
  else
    info "Installing/updating Playwright Python dependency..."
    python -m pip install -e ".[browser]"
    write_marker "${BROWSER_DEPS_MARKER}" "${expected_fingerprint}"
  fi

  if playwright_chromium_ready; then
    info "Playwright Chromium runtime already installed."
  else
    info "Installing Playwright Chromium runtime..."
    python -m playwright install chromium
  fi
}

main() {
  print_header

  require_python
  ensure_venv
  activate_venv

  print_section "Environment Setup"
  info "Using Python environment: ${VENV_DIR}"
  install_base_dependencies_if_needed

  local base_url output_dir pom_language browser_adapter max_depth max_pages headed_flag
  print_section "Run Configuration"
  base_url="$(prompt_url "https://vinipx.github.io/AUTOPOM/")"
  output_dir="$(prompt_default "Output directory" "output-live")"
  pom_language="$(choose_from_list "Choose POM output language:" 3 "java" "javascript" "typescript")"
  browser_adapter="$(choose_from_list "Choose browser adapter:" 2 "mock" "playwright")"
  echo "Max crawl depth defines link traversal levels from the base URL."
  echo "Example: depth 1 = direct links only, depth 2 = links from those pages."
  max_depth="$(prompt_positive_int "Max crawl depth" "2")"
  echo "Max pages to model limits how many unique pages AUTOPOM persists per run."
  max_pages="$(prompt_positive_int "Max pages to model" "20")"
  headed_flag=""

  if [[ "${browser_adapter}" == "playwright" ]]; then
    print_section "Playwright Runtime Setup"
    ensure_playwright_ready
    if prompt_yes_no "Run in headed mode (visible browser window)?" "n"; then
      headed_flag="--headed"
    fi
  fi

  print_section "Execution Preview"
  echo "Base URL        : ${base_url}"
  echo "Output Dir      : ${output_dir}"
  echo "POM Language    : ${pom_language}"
  echo "Browser Adapter : ${browser_adapter}"
  echo "Max Depth       : ${max_depth}"
  echo "Max Pages       : ${max_pages}"
  if [[ -n "${headed_flag}" ]]; then
    echo "Headless Mode   : false"
  else
    echo "Headless Mode   : true"
  fi

  local cmd=(
    python -m autopom.cli.main
    --base-url "${base_url}"
    --output-dir "${output_dir}"
    --pom-language "${pom_language}"
    --browser-adapter "${browser_adapter}"
    --max-depth "${max_depth}"
    --max-pages "${max_pages}"
  )
  if [[ -n "${headed_flag}" ]]; then
    cmd+=("${headed_flag}")
  fi

  echo
  info "Command preview:"
  echo "PYTHONPATH=src ${cmd[*]}"
  echo

  if ! prompt_yes_no "Proceed with execution?" "y"; then
    warn "Execution canceled by user."
    exit 0
  fi

  echo
  info "Running AUTOPOM ..."
  PYTHONPATH=src "${cmd[@]}"
  echo
  info "Done. Check output under: ${output_dir}"
}

main "$@"
