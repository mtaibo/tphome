#!/bin/bash
set -e

ENVS=(blind_esp8266 blind_bk7231n light_bk7231)

if ! command -v pio &>/dev/null; then
  echo "Error: PlatformIO not found. Install it with: pip install platformio"
  exit 1
fi

case "${1:-blind_esp8266}" in
  all)
    for env in "${ENVS[@]}"; do
      echo "Building $env..."
      pio run -e "$env"
    done
    ;;
  blind_esp8266|blind_bk7231n|light_bk7231)
    pio run -e "$1"
    ;;
  flash)
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
