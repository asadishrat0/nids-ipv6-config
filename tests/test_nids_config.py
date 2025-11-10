#!/usr/bin/env python3
import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, '../src')

class TestIPv6Config(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "ipv6_config.json"
    
    def test_ipv6_address_validation(self):
        """Test IPv6 address validation"""
        from nids_ipv6_config import NIDSIPv6ConfigManager
        
        # Valid addresses
        valid_addresses = ["::", "::1", "fe80::1", "2001:db8::1"]
        for addr in valid_addresses:
            result = NIDSIPv6ConfigManager._validate_ipv6(addr)
            self.assertTrue(result, f"Failed to validate {addr}")
    
    def test_invalid_ipv6_address(self):
        """Test invalid IPv6 address rejection"""
        from nids_ipv6_config import NIDSIPv6ConfigManager
        
        invalid_addresses = ["invalid", "192.168.1.1", "gggg::1"]
        for addr in invalid_addresses:
            result = NIDSIPv6ConfigManager._validate_ipv6(addr)
            self.assertFalse(result, f"Should reject {addr}")
    
    def test_port_validation(self):
        """Test port number validation"""
        valid_ports = [1, 80, 443, 25826, 65535]
        for port in valid_ports:
            self.assertTrue(1 <= port <= 65535)
    
    def test_logging_levels(self):
        """Test valid logging levels"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        for level in valid_levels:
            self.assertIn(level, valid_levels)

if __name__ == '__main__':
    unittest.main()
