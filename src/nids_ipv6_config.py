#!/usr/bin/env python3
"""
NIDS IPv6 Configuration Application
"""

import json
import os
import sys
import argparse
import logging
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass, asdict
import tempfile

# Use temp directory for configuration and logs
TEMP_DIR = Path(tempfile.gettempdir()) / "nids"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_FILE = TEMP_DIR / "ipv6_config.json"
LOG_FILE = TEMP_DIR / "ipv6_config.log"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@dataclass
class IPv6Config:
    """IPv6 Configuration Data Model"""
    ipv6_enabled: bool = True
    listen_address: str = "::"
    listen_port: int = 25826
    monitoring_enabled: bool = True
    traffic_rules_enabled: bool = True
    logging_level: str = "INFO"
    max_packet_size: int = 65535
    pcap_filter: str = "ip6"
    alert_threshold: int = 100
    stats_interval: int = 60


class NIDSIPv6ConfigManager:
    """Manages NIDS IPv6 configuration"""
    
    def __init__(self):
        """Initialize configuration manager"""
        self.config = IPv6Config()
        self.config_file = CONFIG_FILE
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.config = IPv6Config(**data)
                logger.info(f"Configuration loaded")
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
                self._save_config()
        else:
            logger.info("Creating default configuration")
            self._save_config()
    
    def _save_config(self) -> None:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(asdict(self.config), f, indent=2)
            logger.info(f"Configuration saved")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def enable_ipv6(self) -> None:
        """Enable IPv6 monitoring"""
        self.config.ipv6_enabled = True
        self._save_config()
        logger.info("IPv6 enabled")
    
    def disable_ipv6(self) -> None:
        """Disable IPv6 monitoring"""
        self.config.ipv6_enabled = False
        self._save_config()
        logger.info("IPv6 disabled")
    
    def set_listen_address(self, address: str) -> None:
        """Set IPv6 listen address"""
        if not self._validate_ipv6(address):
            raise ValueError(f"Invalid IPv6 address: {address}")
        self.config.listen_address = address
        self._save_config()
        logger.info(f"Address set to {address}")
    
    def set_listen_port(self, port: int) -> None:
        """Set listen port"""
        if not (1 <= port <= 65535):
            raise ValueError(f"Invalid port: {port}")
        self.config.listen_port = port
        self._save_config()
        logger.info(f"Port set to {port}")
    
    def set_logging_level(self, level: str) -> None:
        """Set logging level"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if level.upper() not in valid_levels:
            raise ValueError(f"Invalid level: {level}")
        self.config.logging_level = level.upper()
        self._save_config()
        logger.info(f"Log level set to {level}")
    
    def set_pcap_filter(self, filter_str: str) -> None:
        """Set packet capture filter"""
        self.config.pcap_filter = filter_str
        self._save_config()
        logger.info(f"PCAP filter set")
    
    def enable_traffic_rules(self) -> None:
        """Enable traffic rules"""
        self.config.traffic_rules_enabled = True
        self._save_config()
        logger.info("Traffic rules enabled")
    
    def disable_traffic_rules(self) -> None:
        """Disable traffic rules"""
        self.config.traffic_rules_enabled = False
        self._save_config()
        logger.info("Traffic rules disabled")
    
    def enable_monitoring(self) -> None:
        """Enable monitoring"""
        self.config.monitoring_enabled = True
        self._save_config()
        logger.info("Monitoring enabled")
    
    def disable_monitoring(self) -> None:
        """Disable monitoring"""
        self.config.monitoring_enabled = False
        self._save_config()
        logger.info("Monitoring disabled")
    
    def set_alert_threshold(self, threshold: int) -> None:
        """Set alert threshold"""
        if threshold < 1:
            raise ValueError(f"Threshold must be positive")
        self.config.alert_threshold = threshold
        self._save_config()
        logger.info(f"Alert threshold set")
    
    def set_stats_interval(self, interval: int) -> None:
        """Set statistics interval"""
        if interval < 1:
            raise ValueError(f"Interval must be positive")
        self.config.stats_interval = interval
        self._save_config()
        logger.info(f"Stats interval set")
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return asdict(self.config)
    
    def show_config(self) -> str:
        """Display configuration"""
        config_dict = self.get_config()
        output = "\n=== NIDS IPv6 Configuration ===\n"
        for key, value in config_dict.items():
            output += f"{key:.<30} {value}\n"
        output += "=" * 35 + "\n"
        return output
    
    def validate_configuration(self) -> bool:
        """Validate configuration"""
        try:
            if not isinstance(self.config.ipv6_enabled, bool):
                raise ValueError("ipv6_enabled must be boolean")
            if not (1 <= self.config.listen_port <= 65535):
                raise ValueError("port out of range")
            if self.config.logging_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
                raise ValueError("invalid log level")
            logger.info("Validation successful")
            return True
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            return False
    
    @staticmethod
    def _validate_ipv6(address: str) -> bool:
        """Validate IPv6 address"""
        try:
            import ipaddress
            ipaddress.IPv6Address(address)
            return True
        except ValueError:
            return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="NIDS IPv6 Configuration Manager"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    subparsers.add_parser('show', help='Show configuration')
    subparsers.add_parser('enable', help='Enable IPv6')
    subparsers.add_parser('disable', help='Disable IPv6')
    
    address_parser = subparsers.add_parser('set-address', help='Set address')
    address_parser.add_argument('address', help='IPv6 address')
    
    port_parser = subparsers.add_parser('set-port', help='Set port')
    port_parser.add_argument('port', type=int, help='Port number')
    
    log_parser = subparsers.add_parser('set-log-level', help='Set log level')
    log_parser.add_argument('level', help='Log level')
    
    pcap_parser = subparsers.add_parser('set-pcap-filter', help='Set PCAP filter')
    pcap_parser.add_argument('filter', help='PCAP filter')
    
    subparsers.add_parser('enable-rules', help='Enable rules')
    subparsers.add_parser('disable-rules', help='Disable rules')
    subparsers.add_parser('enable-monitoring', help='Enable monitoring')
    subparsers.add_parser('disable-monitoring', help='Disable monitoring')
    
    threshold_parser = subparsers.add_parser('set-alert-threshold', help='Set threshold')
    threshold_parser.add_argument('threshold', type=int, help='Threshold value')
    
    stats_parser = subparsers.add_parser('set-stats-interval', help='Set stats interval')
    stats_parser.add_argument('interval', type=int, help='Interval seconds')
    
    subparsers.add_parser('validate', help='Validate config')
    
    args = parser.parse_args()
    
    try:
        manager = NIDSIPv6ConfigManager()
        
        if args.command == 'show':
            print(manager.show_config())
        elif args.command == 'enable':
            manager.enable_ipv6()
            print("✓ IPv6 enabled")
        elif args.command == 'disable':
            manager.disable_ipv6()
            print("✓ IPv6 disabled")
        elif args.command == 'set-address':
            manager.set_listen_address(args.address)
            print(f"✓ Address set to {args.address}")
        elif args.command == 'set-port':
            manager.set_listen_port(args.port)
            print(f"✓ Port set to {args.port}")
        elif args.command == 'set-log-level':
            manager.set_logging_level(args.level)
            print(f"✓ Log level set to {args.level}")
        elif args.command == 'set-pcap-filter':
            manager.set_pcap_filter(args.filter)
            print(f"✓ PCAP filter set")
        elif args.command == 'enable-rules':
            manager.enable_traffic_rules()
            print("✓ Rules enabled")
        elif args.command == 'disable-rules':
            manager.disable_traffic_rules()
            print("✓ Rules disabled")
        elif args.command == 'enable-monitoring':
            manager.enable_monitoring()
            print("✓ Monitoring enabled")
        elif args.command == 'disable-monitoring':
            manager.disable_monitoring()
            print("✓ Monitoring disabled")
        elif args.command == 'set-alert-threshold':
            manager.set_alert_threshold(args.threshold)
            print(f"✓ Threshold set")
        elif args.command == 'set-stats-interval':
            manager.set_stats_interval(args.interval)
            print(f"✓ Stats interval set")
        elif args.command == 'validate':
            if manager.validate_configuration():
                print("✓ Configuration is valid")
            else:
                print("✗ Configuration validation failed")
                sys.exit(1)
        else:
            parser.print_help()
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
