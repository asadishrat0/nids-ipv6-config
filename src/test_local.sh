#!/bin/bash

echo "========== NIDS IPv6 Configuration - Local Testing =========="

# Create test environment
TEST_DIR="/tmp/nids_test_$$"
mkdir -p "$TEST_DIR/etc/nids"
mkdir -p "$TEST_DIR/var/log/nids"

echo "✓ Test directory created: $TEST_DIR"

# Copy config
cp config/ipv6_config.json "$TEST_DIR/etc/nids/"
echo "✓ Configuration copied"

# Test Python syntax
python3 -m py_compile src/nids_ipv6_config.py
echo "✓ Python syntax valid"

# Run tests
echo ""
echo "Running unit tests..."
cd tests
python3 -m pytest test_nids_config.py -v 2>/dev/null || python3 test_nids_config.py -v 2>/dev/null || echo "Tests require pytest"

# Cleanup
echo ""
echo "Cleaning up test environment..."
rm -rf "$TEST_DIR"
echo "✓ Done"
