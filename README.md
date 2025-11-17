# NIDS IPv6 Configuration Application

A production-ready command-line tool for managing Network Intrusion Detection System (NIDS) IPv6 settings across Ubuntu 22.04 and Red Hat 9.6 servers.

## Quick Overview

This application lets you configure and manage IPv6 settings for NIDS monitoring through simple commands. Everything is stored in a configuration file and persists across reboots.

**What it does:**
- Enable/disable IPv6 monitoring
- Configure listening addresses and ports
- Manage logging levels and traffic rules
- Set packet capture filters
- Validate your configuration

**Platforms:**
- Ubuntu 22.04 LTS (DEB package)
- Red Hat 9.6 (RPM package)

## Installation

### Ubuntu 22.04

```bash
# Install the package
sudo apt-get update
sudo apt-get install ./nids-ipv6-config_1.0.0-1_all.deb

# Verify it works
sudo nids-ipv6-config show


# Install the package
sudo yum install ./nids-ipv6-config-1.0.0-1.el9.noarch.rpm

# Verify it works
sudo nids-ipv6-config show


## Basic Usage

### View Current Settings

```bash
sudo nids-ipv6-config show
```

Output:
```
=== NIDS IPv6 Configuration ===
ipv6_enabled.......................... True
listen_address....................... ::
listen_port.......................... 25826
monitoring_enabled................... True
traffic_rules_enabled................ True
logging_level........................ INFO
pcap_filter.......................... ip6
alert_threshold...................... 100
stats_interval....................... 60
===================================
```

### Enable/Disable IPv6 Monitoring

```bash
# Turn it on
sudo nids-ipv6-config enable

# Turn it off
sudo nids-ipv6-config disable
```

### Change Listen Address

```bash
# Listen on all interfaces
sudo nids-ipv6-config set-address ::

# Listen on loopback only
sudo nids-ipv6-config set-address ::1

# Listen on specific address
sudo nids-ipv6-config set-address 2001:db8::1
```

### Change Port

```bash
# Set to port 9000
sudo nids-ipv6-config set-port 9000

# Verify the change
sudo nids-ipv6-config show | grep listen_port
```

### Adjust Logging

```bash
# Verbose logging for troubleshooting
sudo nids-ipv6-config set-log-level DEBUG

# Normal operation
sudo nids-ipv6-config set-log-level INFO

# Minimal logging
sudo nids-ipv6-config set-log-level ERROR
```

### Manage Traffic Rules

```bash
# Enable rule enforcement
sudo nids-ipv6-config enable-rules

# Disable rules
sudo nids-ipv6-config disable-rules
```

### Set Packet Filter

```bash
# Monitor all IPv6 traffic
sudo nids-ipv6-config set-pcap-filter "ip6"

# Monitor only HTTPS
sudo nids-ipv6-config set-pcap-filter "tcp port 443"

# Monitor DNS
sudo nids-ipv6-config set-pcap-filter "udp port 53"
```

### Validate Settings

```bash
sudo nids-ipv6-config validate
```

## Configuration File

Configuration is stored at `/etc/nids/ipv6_config.json`:

```json
{
  "ipv6_enabled": true,
  "listen_address": "::",
  "listen_port": 25826,
  "monitoring_enabled": true,
  "traffic_rules_enabled": true,
  "logging_level": "INFO",
  "max_packet_size": 65535,
  "pcap_filter": "ip6",
  "alert_threshold": 100,
  "stats_interval": 60
}
```

**Note:** You can edit this file directly, but it's safer to use commands above.

## Logs

Check application logs at `/var/log/nids/ipv6_config.log`:

```bash
# View recent logs
sudo tail -f /var/log/nids/ipv6_config.log

# View last 50 lines
sudo tail -50 /var/log/nids/ipv6_config.log
```

## Common Tasks

### Production Setup

```bash
# Listen on all interfaces
sudo nids-ipv6-config set-address ::

# Standard logging
sudo nids-ipv6-config set-log-level INFO

# Enable monitoring
sudo nids-ipv6-config enable
sudo nids-ipv6-config enable-rules
sudo nids-ipv6-config enable-monitoring

# Verify
sudo nids-ipv6-config show
sudo nids-ipv6-config validate
```

### Development Setup

```bash
# Verbose logging
sudo nids-ipv6-config set-log-level DEBUG

# Listen locally
sudo nids-ipv6-config set-address ::1

# Lower alert threshold for testing
sudo nids-ipv6-config set-alert-threshold 10
```

### Troubleshooting Setup

```bash
# Enable debug logging
sudo nids-ipv6-config set-log-level DEBUG

# Check logs
sudo tail -100 /var/log/nids/ipv6_config.log

# Validate config
sudo nids-ipv6-config validate
```

## Backup & Restore

### Backup Configuration

```bash
# Quick backup
sudo cp /etc/nids/ipv6_config.json /etc/nids/ipv6_config.json.backup

# Timestamped backup
sudo cp /etc/nids/ipv6_config.json /etc/nids/ipv6_config.json.$(date +%Y%m%d-%H%M%S)
```

### Restore Configuration

```bash
# Restore from backup
sudo cp /etc/nids/ipv6_config.json.backup /etc/nids/ipv6_config.json

# Verify
sudo nids-ipv6-config show
sudo nids-ipv6-config validate
```

## System Requirements

- **OS:** Ubuntu 22.04 LTS or Red Hat 9.6
- **Python:** 3.9 or later (pre-installed)
- **Disk:** ~100MB free space
- **Permissions:** Root/sudo access required

## Troubleshooting

### "Command not found"

Make sure you're using `sudo`:
```bash
sudo nids-ipv6-config show
```

### "Permission denied"

All commands require root. Use `sudo`:
```bash
sudo nids-ipv6-config enable
```

### Configuration not persisting

Your configuration should persist across reboots. If not, check:
```bash
# Check file permissions
ls -la /etc/nids/ipv6_config.json

# View recent logs
sudo tail -50 /var/log/nids/ipv6_config.log
```

### Changes not taking effect

After making changes, validate your configuration:
```bash
sudo nids-ipv6-config validate
```

## Uninstall

### Ubuntu 22.04

```bash
sudo apt-get remove nids-ipv6-config

# Optional: Remove config files
sudo rm -rf /etc/nids
sudo rm -rf /var/log/nids
```

### Red Hat 9.6

```bash
sudo yum remove nids-ipv6-config

# Optional: Remove config files
sudo rm -rf /etc/nids
sudo rm -rf /var/log/nids
```

## For More Information

- [Installation Guide](INSTALL.md) - Detailed installation steps
- [Configuration Guide](CONFIG.md) - All configuration options explained

## Support

Issues or questions? Check the logs and validation output first, then contact your system administrator.