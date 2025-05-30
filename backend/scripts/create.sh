#!/usr/bin/env bash
set -e

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Infer the project root directory (assuming the script is in backend/scripts/)
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"

if [ $# -eq 0 ]; then
    echo "Usage: $0 <router_name>"
    exit 1
fi

ROUTER_NAME=$1
ROUTER_PATH="$PROJECT_ROOT/backend/app/$ROUTER_NAME"
TEST_PATH="$PROJECT_ROOT/backend/tests/$ROUTER_NAME"

# Create the router directory
mkdir -p "$ROUTER_PATH"

# Create the files
touch "$ROUTER_PATH/__init__.py"
touch "$ROUTER_PATH/config.py"
touch "$ROUTER_PATH/constants.py"
touch "$ROUTER_PATH/dependencies.py"
touch "$ROUTER_PATH/exceptions.py"
touch "$ROUTER_PATH/models.py"
touch "$ROUTER_PATH/routes.py"
touch "$ROUTER_PATH/schemas.py"
touch "$ROUTER_PATH/service.py"
touch "$ROUTER_PATH/utils.py"

# Create the test directory and files
mkdir -p "$TEST_PATH"
touch "$TEST_PATH/__init__.py"
touch "$TEST_PATH/test_service.py"

echo "Router '$ROUTER_NAME' created successfully at $ROUTER_PATH"
echo "Test files for '$ROUTER_NAME' created successfully at $TEST_PATH"
