#!/usr/bin/env python3
"""
NIDS IPv6 Configuration Application
Manages IPv6 network intrusion detection system settings on Ubuntu 22.04 LTS and Red Hat 9.6
"""

import json
import os
import sys
import argparse
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import tempfile

# Configuration paths - Use temp directory if /var/log/nids not available
CONFIG_DIR = Path("/etc/nids")
CONFIG_FILE = CONFIG_DIR / "ipv6_config.json"

# Use temp directory for logs if /var/log/nids is not writable
try:
    LOG_DIR = Path("/var/log/nids")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
except PermissionError:
    LOG_DIR = Path(tempfile.gettempdir()) / "nids"
    LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "ipv6_config.log"

# Setup logging
try:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
except Exception:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
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
        self._ensure_directories()
        self._load_config()
    
    def _ensure_directories(self) -> None:
        """Ensure required directories exist"""
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            logger.info(f"Directories ensured: {CONFIG_DIR}, {LOG_DIR}")
        except Exception as e:
            logger.warning(f"Could not create directories: {e}")
    
    def _load_config(self) -> None:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.config = IPv6Config(**data)
                logger.info(f"Configuration loaded from {self.config_file}")
            except Exception as e:
                logger.error(f"Failed to load config: {e}. Using defaults.")
                self._save_config()
        else:
            logger.info("No existing config found. Creating with defaults.")
            try:
                self._save_config()
            except Exception as e:
                logger.warning(f"Could not save config: {e}")
    
    def _save_config(self) -> None:
        """Save configuration to file"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(asdict(self.config), f, indent=2)
            try:
                os.chmod(self.config_file, 0o640)
            except Exception:
                pass
            logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def enable_ipv6(self) -> None:
        """Enable IPv6 monitoring"""
        self.config.ipv6_enabled = True
        self._save_config()
        logger.info("IPv6 monitoring enabled")
    
    def disable_ipv6(self) -> None:
        """Disable IPv6 monitoring"""
        self.config.ipv6_enabled = False
        self._save_config()
        logger.info("IPv6 monitoring disabled")
    
    def set_listen_address(self, address: str) -> None:
        """Set IPv6 listen address"""
        if not self._validate_ipv6(address):
            raise ValueError(f"Invalid IPv6 address: {address}")
        self.config.listen_address = address
        self._save_config()
        logger.info(f"Listen address set to {address}")
    
    def set_listen_port(self, port: int) -> None:
        """Set listen port"""
        if not (1 <= port <= 65535):
            raise ValueError(f"Invalid port number: {port}")
        self.config.listen_port = port
        self._save_config()
        logger.info(f"Listen port set to {port}")
    
    def set_logging_level(self, level: str) -> None:
        """Set logging level"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if level.upper() not in valid_levels:
            raise ValueError(f"Invalid logging level: {level}")
        self.config.logging_level = level.upper()
        self._save_config()
        logger.info(f"Logging level set to {level}")
    
    def set_pcap_filter(self, filter_str: str) -> None:
        """Set packet capture filter"""
        self.config.pcap_filter = filter_str
        self._save_config()
        logger.info(f"PCAP filter set to {filter_str}")
    
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
            raise ValueError(f"Alert threshold must be positive: {threshold}")
        self.config.alert_threshold = threshold
        self._save_config()
        logger.info(f"Alert threshold set to {threshold}")
    
    def set_stats_interval(self, interval: int) -> None:
        """Set statistics interval"""
        if interval < 1:
            raise ValueError(f"Stats interval must be positive: {interval}")
        self.config.stats_interval = interval
        self._save_config()
        logger.info(f"Stats interval set to {interval}")
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return asdict(self.config)
    
    def show_config(self) -> str:
        """Display configuration in formatted way"""
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
                raise ValueError("listen_port out of range")
            if self.config.logging_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
                raise ValueError("invalid logging_level")
            if self.config.alert_threshold < 1:
                raise ValueError("alert_threshold must be positive")
            logger.info("Configuration validation successful")
            return True
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
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
        description="NIDS IPv6 Configuration Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  nids-ipv6-config show
  nids-ipv6-config enable
  nids-ipv6-config disable
  nids-ipv6-config set-address ::
  nids-ipv6-config set-port 25826
  nids-ipv6-config set-log-level DEBUG
  nids-ipv6-config validate
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    subparsers.add_parser('show', help='Show current configuration')
    subparsers.add_parser('enable', help='Enable IPv6 monitoring')
    subparsers.add_parser('disable', help='Disable IPv6 monitoring')
    
    address_parser = subparsers.add_parser('set-address', help='Set IPv6 listen address')
    address_parser.add_argument('address', help='IPv6 address (e.g., ::, ::1)')
    
    port_parser = subparsers.add_parser('set-port', help='Set listen port')
    port_parser.add_argument('port', type=int, help='Port number (1-65535)')
    
    log_parser = subparsers.add_parser('set-log-level', help='Set logging level')
    log_parser.add_argument('level', help='Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
    
    pcap_parser = subparsers.add_parser('set-pcap-filter', help='Set PCAP filter')
    pcap_parser.add_argument('filter', help='PCAP filter expression')
    
    subparsers.add_parser('enable-rules', help='Enable traffic rules')
    subparsers.add_parser('disable-rules', help='Disable traffic rules')
    subparsers.add_parser('enable-monitoring', help='Enable monitoring')
    subparsers.add_parser('disable-monitoring', help='Disable monitoring')
    
    threshold_parser = subparsers.add_parser('set-alert-threshold', help='Set alert threshold')
    threshold_parser.add_argument('threshold', type=int, help='Alert threshold value')
    
    stats_parser = subparsers.add_parser('set-stats-interval', help='Set statistics interval')
    stats_parser.add_argument('interval', type=int, help='Interval in seconds')
    
    subparsers.add_parser('validate', help='Validate configuration')
    
    args = parser.parse_args()
    
    if os.name != 'nt':
        if os.geteuid() != 0 and args.command not in ['show', 'validate', None]:
            print("Error: This command requires root privileges")
            sys.exit(1)
    
    try:
        manager = NIDSIPv6ConfigManager()
        
        if args.command == 'show':
            print(manager.show_config())
        elif args.command == 'enable':
            manager.enable_ipv6()
            print("✓ IPv6 monitoring enabled")
        elif args.command == 'disable':
            manager.disable_ipv6()
            print("✓ IPv6 monitoring disabled")
        elif args.command == 'set-address':
            manager.set_listen_address(args.address)
            print(f"✓ Listen address set to {args.address}")
        elif args.command == 'set-port':
            manager.set_listen_port(args.port)
            print(f"✓ Listen port set to {args.port}")
        elif args.command == 'set-log-level':
            manager.set_logging_level(args.level)
            print(f"✓ Logging level set to {args.level}")
        elif args.command == 'set-pcap-filter':
            manager.set_pcap_filter(args.filter)
            print(f"✓ PCAP filter set to {args.filter}")
        elif args.command == 'enable-rules':
            manager.enable_traffic_rules()
            print("✓ Traffic rules enabled")
        elif args.command == 'disable-rules':
            manager.disable_traffic_rules()
            print("✓ Traffic rules disabled")
        elif args.command == 'enable-monitoring':
            manager.enable_monitoring()
            print("✓ Monitoring enabled")
        elif args.command == 'disable-monitoring':
            manager.disable_monitoring()
            print("✓ Monitoring disabled")
        elif args.command == 'set-alert-threshold':
            manager.set_alert_threshold(args.threshold)
            print(f"✓ Alert threshold set to {args.threshold}")
        elif args.command == 'set-stats-interval':
            manager.set_stats_interval(args.interval)
            print(f"✓ Stats interval set to {args.interval}")
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
