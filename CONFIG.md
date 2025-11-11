# NIDS IPv6 Configuration Application - Configuration Guide

## Configuration Overview

The NIDS IPv6 Configuration Application stores all settings in JSON format at `/etc/nids/ipv6_config.json`. This guide explains each configuration parameter and how to adjust them for your environment.

## Configuration File Location

```bash
# View current configuration
sudo cat /etc/nids/ipv6_config.json

# Edit configuration manually
sudo vi /etc/nids/ipv6_config.json
```

## Configuration Parameters

### 1. IPv6 Enablement

**Parameter:** `ipv6_enabled`  
**Type:** Boolean  
**Default:** `true`  
**Description:** Controls whether IPv6 monitoring is active.

```bash
# Enable IPv6
sudo nids-ipv6-config enable

# Disable IPv6
sudo nids-ipv6-config disable
```

### 2. Listen Address

**Parameter:** `listen_address`  
**Type:** IPv6 Address  
**Default:** `::`  
**Description:** IPv6 address on which the NIDS listens for connections.

Valid values:
- `::` - All IPv6 interfaces
- `::1` - Loopback interface
- `fe80::1` - Link-local address
- `2001:db8::1` - Global unicast address

```bash
# Set to listen on loopback only
sudo nids-ipv6-config set-address ::1

# Set to listen on all interfaces
sudo nids-ipv6-config set-address ::

# Set to specific address
sudo nids-ipv6-config set-address 2001:db8::1
```

### 3. Listen Port

**Parameter:** `listen_port`  
**Type:** Integer (1-65535)  
**Default:** `25826`  
**Description:** Network port on which the NIDS listens.

Port Selection Guidelines:
- Privileged ports (1-1023): Require root access
- Ephemeral ports (49152-65535): May conflict with system services
- Common NIDS ports: 25826 (default), 514 (syslog alternative)

```bash
# Set to standard NIDS port
sudo nids-ipv6-config set-port 25826

# Set to custom port
sudo nids-ipv6-config set-port 9000

# Verify port change
sudo nids-ipv6-config show | grep listen_port
```

### 4. Monitoring Enablement

**Parameter:** `monitoring_enabled`  
**Type:** Boolean  
**Default:** `true`  
**Description:** Enables or disables packet monitoring functionality.

```bash
# Enable monitoring
sudo nids-ipv6-config enable-monitoring

# Disable monitoring
sudo nids-ipv6-config disable-monitoring
```

### 5. Traffic Rules

**Parameter:** `traffic_rules_enabled`  
**Type:** Boolean  
**Default:** `true`  
**Description:** Controls enforcement of traffic filtering rules.

```bash
# Enable traffic rules
sudo nids-ipv6-config enable-rules

# Disable traffic rules
sudo nids-ipv6-config disable-rules
```

### 6. Logging Level

**Parameter:** `logging_level`  
**Type:** String  
**Default:** `INFO`  
**Options:** DEBUG, INFO, WARNING, ERROR, CRITICAL

Description: Controls verbosity of application logging.

| Level | Use Case |
|-------|----------|
| DEBUG | Development, detailed troubleshooting |
| INFO | Normal operations, standard events |
| WARNING | Unusual conditions, potential issues |
| ERROR | Error conditions, failures |
| CRITICAL | Critical failures only |

```bash
# Set to DEBUG (verbose)
sudo nids-ipv6-config set-log-level DEBUG

# Set to INFO (standard)
sudo nids-ipv6-config set-log-level INFO

# Set to ERROR (minimal)
sudo nids-ipv6-config set-log-level ERROR

# View logs
tail -f /var/log/nids/ipv6_config.log
```

### 7. Maximum Packet Size

**Parameter:** `max_packet_size`  
**Type:** Integer (bytes)  
**Default:** `65535`  
**Description:** Maximum size of packets to process (MTU consideration).

Standard values:
- `65535` - Jumbo frames / full IPv6 payload
- `9000` - Jumbo frames (Ethernet)
- `1500` - Standard Ethernet MTU
- `1280` - IPv6 minimum MTU

```bash
# For standard networks
sudo python3 -c "
import json
with open('/etc/nids/ipv6_config.json', 'r') as f:
    config = json.load(f)
config['max_packet_size'] = 1500
with open('/etc/nids/ipv6_config.json', 'w') as f:
    json.dump(config, f, indent=2)
"

# Verify change
sudo nids-ipv6-config show
```

### 8. PCAP Filter

**Parameter:** `pcap_filter`  
**Type:** String (BPF syntax)  
**Default:** `ip6`  
**Description:** Packet capture filter expression (Berkeley Packet Filter format).

Common filter examples:
- `ip6` - All IPv6 traffic
- `tcp port 443` - HTTPS traffic
- `tcp or udp` - TCP and UDP traffic
- `icmpv6` - ICMPv6 traffic
- `dst 2001:db8::/32` - Specific subnet

```bash
# Monitor all IPv6
sudo nids-ipv6-config set-pcap-filter "ip6"

# Monitor HTTPS only
sudo nids-ipv6-config set-pcap-filter "tcp port 443"

# Monitor DNS
sudo nids-ipv6-config set-pcap-filter "udp port 53"

# Monitor specific subnet
sudo nids-ipv6-config set-pcap-filter "dst 2001:db8::/32"
```

### 9. Alert Threshold

**Parameter:** `alert_threshold`  
**Type:** Integer (events)  
**Default:** `100`  
**Description:** Number of suspicious events before triggering alert.

```bash
# Set to trigger on 50 events
sudo nids-ipv6-config set-alert-threshold 50

# Set to trigger on 500 events
sudo nids-ipv6-config set-alert-threshold 500

# Verify
sudo nids-ipv6-config show | grep alert_threshold
```

### 10. Statistics Interval

**Parameter:** `stats_interval`  
**Type:** Integer (seconds)  
**Default:** `60`  
**Description:** Interval for generating performance statistics.

```bash
# Update statistics every 30 seconds
sudo nids-ipv6-config set-stats-interval 30

# Update statistics every 5 minutes
sudo nids-ipv6-config set-stats-interval 300

# Verify
sudo nids-ipv6-config show | grep stats_interval
```

## Configuration Scenarios

### Scenario 1: Development Environment

```bash
# Enable verbose logging
sudo nids-ipv6-config set-log-level DEBUG

# Listen on loopback
sudo nids-ipv6-config set-address ::1

# Lower alert threshold for testing
sudo nids-ipv6-config set-alert-threshold 10

# More frequent stats
sudo nids-ipv6-config set-stats-interval 10
```

### Scenario 2: Production High-Traffic Network

```bash
# Standard logging
sudo nids-ipv6-config set-log-level INFO

# Listen on all interfaces
sudo nids-ipv6-config set-address ::

# Higher alert threshold
sudo nids-ipv6-config set-alert-threshold 500

# Less frequent stats
sudo nids-ipv6-config set-stats-interval 300

# Monitor all IPv6 traffic
sudo nids-ipv6-config set-pcap-filter "ip6"
```

### Scenario 3: Compliance Monitoring

```bash
# Detailed logging for audit trail
sudo nids-ipv6-config set-log-level DEBUG

# Monitor all traffic
sudo nids-ipv6-config set-pcap-filter "ip6"

# Lower threshold for compliance
sudo nids-ipv6-config set-alert-threshold 50

# Enable all monitoring
sudo nids-ipv6-config enable-monitoring
sudo nids-ipv6-config enable-rules
```

### Scenario 4: Specific Protocol Monitoring

```bash
# Monitor only HTTPS
sudo nids-ipv6-config set-pcap-filter "tcp port 443"
sudo nids-ipv6-config set-log-level INFO

# Monitor DNS queries
sudo nids-ipv6-config set-pcap-filter "udp port 53"

# Monitor ICMP6 (ping, neighbor discovery)
sudo nids-ipv6-config set-pcap-filter "icmpv6"
```

## Manual Configuration File Editing

For advanced users, configuration can be edited directly:

```bash
# Backup current configuration
sudo cp /etc/nids/ipv6_config.json /etc/nids/ipv6_config.json.bak

# Edit configuration
sudo nano /etc/nids/ipv6_config.json

# Validate after editing
sudo nids-ipv6-config validate

# Restore if validation fails
sudo cp /etc/nids/ipv6_config.json.bak /etc/nids/ipv6_config.json
```

Example configuration:

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

## Configuration Validation

Always validate configuration after changes:

```bash
# Validate configuration
sudo nids-ipv6-config validate

# Expected output on success
# ✓ Configuration is valid
```

## Troubleshooting Configuration

### Issue: Invalid IPv6 Address

```bash
# Wrong format
sudo nids-ipv6-config set-address invalid

# Error output
# Error: Invalid IPv6 address: invalid

# Correct format
sudo nids-ipv6-config set-address ::1
```

### Issue: Port Out of Range

```bash
# Port too high
sudo nids-ipv6-config set-port 99999

# Error output
# Error: Invalid port number: 99999

# Valid port
sudo nids-ipv6-config set-port 25826
```

### Issue: Validation Fails

```bash
# Run validation with details
sudo nids-ipv6-config validate

# Check logs for errors
sudo tail -50 /var/log/nids/ipv6_config.log

# Reset to defaults
sudo rm /etc/nids/ipv6_config.json
sudo nids-ipv6-config show
```

## Configuration Persistence

Configuration changes persist across system reboots:

```bash
# Make change
sudo nids-ipv6-config set-port 9000

# Reboot
sudo reboot

# After reboot, verify configuration persists
sudo nids-ipv6-config show | grep listen_port
```

## Configuration Backup and Recovery

### Backup Current Configuration

```bash
# Create timestamped backup
sudo cp /etc/nids/ipv6_config.json /etc/nids/ipv6_config.json.$(date +%Y%m%d-%H%M%S)

# Archive multiple backups
sudo tar -czf /root/nids_config_backup.tar.gz /etc/nids/
```

### Restore Configuration

```bash
# From backup
sudo cp /etc/nids/ipv6_config.json.20251110-140000 /etc/nids/ipv6_config.json

# Verify restoration
sudo nids-ipv6-config show

# Validate
sudo nids-ipv6-config validate
```

## Performance Tuning

### For High-Volume Traffic

```bash
# Increase packet size for jumbo frames
sudo nids-ipv6-config set-max-packet-size 9000

# Increase stats interval (less overhead)
sudo nids-ipv6-config set-stats-interval 300

# Raise alert threshold to reduce alerts
sudo nids-ipv6-config set-alert-threshold 500
```

### For Detailed Monitoring

```bash
# Enable debug logging
sudo nids-ipv6-config set-log-level DEBUG

# Lower stats interval
sudo nids-ipv6-config set-stats-interval 10

# Lower alert threshold
sudo nids-ipv6-config set-alert-threshold 50
```

## Best Practices

1. **Backup before changes**: Always backup configuration before modifications
2. **Validate after edits**: Run validation command after configuration changes
3. **Test in non-production**: Test new configurations in development first
4. **Document custom settings**: Maintain documentation of custom configurations
5. **Monitor logs**: Regularly review logs for issues
6. **Review periodically**: Periodically review settings for optimization
7. **Use version control**: Store configuration in version control system
