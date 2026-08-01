#!/bin/bash
set -e

ENVS=(blind_esp8266 blind_bk7231n light_bk7231)
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$ROOT/.env"
CREDENTIALS_H="$(dirname "$0")/include/settings/credentials.h"

# Generate credentials.h from root .env
generate_credentials() {
  if [ ! -f "$ENV_FILE" ]; then
    echo "Error: $ENV_FILE not found. Copy .env.example to .env and fill it in."
    exit 1
  fi

  # Parse values from .env (ignore comments and empty lines)
  get() { grep -E "^$1=" "$ENV_FILE" | cut -d= -f2- | tr -d '"' | tr -d "'" | sed 's/[[:space:]]*#.*//' | tr -d '[:space:]'; }

  WIFI_SSID=$(get WIFI_SSID)
  WIFI_PASS=$(get WIFI_PASS)
  MQTT_IP=$(get MQTT_IP)
  MQTT_PORT=$(get MQTT_PORT)
  MQTT_USER=$(get MQTT_USER)
  MQTT_PASS=$(get MQTT_PASS)

  cat > "$CREDENTIALS_H" <<EOF
#ifndef CREDENTIALS_H
#define CREDENTIALS_H

// -----------      WiFi     -------------

#define WIFI_SSID                   "$WIFI_SSID"
#define WIFI_PASS                   "$WIFI_PASS"

// -----------      MQTT     -------------

#define MQTT_IP                     "$MQTT_IP"
#define MQTT_PORT                   ${MQTT_PORT:-1883}
#define MQTT_USER                   "$MQTT_USER"
#define MQTT_PASS                   "$MQTT_PASS"

#endif
EOF
  echo "Generated credentials.h from $ENV_FILE"
}

if ! command -v pio &>/dev/null; then
  echo "Error: PlatformIO not found. Install it with: pip install platformio"
  exit 1
fi

case "${1:-blind_esp8266}" in
  all)
    generate_credentials
    for env in "${ENVS[@]}"; do
      echo "Building $env..."
      pio run -e "$env"
    done
    ;;
  blind_esp8266|blind_bk7231n|light_bk7231)
    generate_credentials
    pio run -e "$1"
    ;;
  flash)
    generate_credentials
    pio run -e "${2:-blind_esp8266}" -t upload
    ;;
  *)
    echo "Usage: ./build.sh [env|all|flash [env]]"
    echo ""
    echo "Environments:"
    for env in "${ENVS[@]}"; do echo "  $env"; done
    echo ""
    echo "Examples:"
    echo "  ./build.sh                    # build blind_esp8266 (default)"
    echo "  ./build.sh all                # build all environments"
    echo "  ./build.sh blind_bk7231n      # build specific environment"
    echo "  ./build.sh flash              # build and flash blind_esp8266"
    echo "  ./build.sh flash blind_bk7231n  # build and flash specific environment"
    exit 1
    ;;
esac
