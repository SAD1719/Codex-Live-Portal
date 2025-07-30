#!/bin/bash

TASK_FILE="../config/task.sync.yaml"
LOG_FILE="../log/task.execution.log"

if [ -z "$1" ]; then
  echo "Usage: $0 <interface_trigger>"
  exit 1
fi

INTERFACE_TRIGGER="$1"
TASK_ID=$(yq e '.tasks[] | select(.interface_trigger == "'$INTERFACE_TRIGGER'") | .id' "$TASK_FILE")
TASK_TITLE=$(yq e '.tasks[] | select(.interface_trigger == "'$INTERFACE_TRIGGER'") | .title' "$TASK_FILE")
TASK_STATUS=$(yq e '.tasks[] | select(.interface_trigger == "'$INTERFACE_TRIGGER'") | .status' "$TASK_FILE")

if [ -z "$TASK_ID" ]; then
  echo "No matching task found for trigger: $INTERFACE_TRIGGER"
  exit 1
fi

# Define route logic based on trigger prefix
case "$INTERFACE_TRIGGER" in
  trust.*)
    TARGET_DIR="../legal"
    ;;
  ledger.*)
    TARGET_DIR="../ledger"
    ;;
  ip.*)
    TARGET_DIR="../ip"
    ;;
  science.*)
    TARGET_DIR="../science"
    ;;
  mirroros.*)
    TARGET_DIR="../scripts"
    ;;
  *)
    TARGET_DIR="../misc"
    ;;
esac

mkdir -p "$TARGET_DIR"
mkdir -p "../log"

# Simulate routing by touching a file
ROUTED_FILE="$TARGET_DIR/${TASK_ID}.routed"
touch "$ROUTED_FILE"

# Log the task execution
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$TIMESTAMP] Routed task '$TASK_TITLE' ($TASK_ID) to $TARGET_DIR" >> "$LOG_FILE"

# Feedback to user
echo "✅ Task '$TASK_TITLE' routed to $TARGET_DIR"
echo "📝 Log updated at $LOG_FILE"
