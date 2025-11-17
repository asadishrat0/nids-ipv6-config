# Configuration Guide

This guide explains all the settings you can configure in the NIDS IPv6 application.

## Configuration Basics

Your settings are stored in: `/etc/nids/ipv6_config.json`

View current config:
```bash
sudo nids-ipv6-config show
```

Edit with commands (recommended):
```bash
sudo nids-ipv6-config set-address ::
sudo nids-ipv6-config set-port 9000
```

Edit manually (advanced):
```bash
# Backup first
sudo cp /etc/nids/ipv6_config.json /etc/nids/ipv6_config.json.backup

# Edit file
sudo nano /etc/nids/ipv6_config.json

# Validate after editing
sudo nids-ipv6-config validate
```

## Settings Reference

### IPv6 Enabled

Controls whether IPv6 monitoring is active.

```bash
# Turn monitoring on
sudo nids-ipv6-config enable

# Turn monitoring off
sudo nids-ipv6-config disable

# Check status
sudo nids-ipv6-config show | grep ipv6_enabled
```

### Listen Address

Which IPv6 address the application listens on.

```bash
# Listen on all interfaces (default)
sudo nids-ipv6-config set-address ::

# Listen on loopback only
sudo nids-ipv6-config set-address ::1

# Listen on specific address
sudo nids-ipv6-config set-address 2001:db8::1

# Listen on link-local address
sudo nids-ipv6-config set-address fe80::1
```

Common addresses:
- `::` - All interfaces
- `::1` - Loopback (local testing)
- `2001:db8::1` - Example global address
- `fe80::1` - Link-local address

### Listen Port

Which port to listen on (1-65535).

```bash
# Standard NIDS port
sudo nids-ipv6-config set-port 25826

# Custom port
sudo nids-ipv6-config set-port 9000

# Check current port
sudo nids-ipv6-config show | grep listen_port
```

Recommended ports:
- `25826` - Default NIDS port
- `514` - Syslog alternative
- `9000-9999` - Custom range

### Monitoring Enabled

Enable or disable packet monitoring.

```bash
# Turn on monitoring
sudo nids-ipv6-config enable-monitoring

# Turn off monitoring
sudo nids-ipv6-config disable-monitoring
```

### Traffic Rules

Enable or disable traffic rule enforcement.

```bash
# Enable rules
sudo nids-ipv6-config enable-rules

# Disable rules
sudo nids-ipv6-config disable-rules
```

### Logging Level

How detailed the logs should be.

```bash
# Very detailed (for troubleshooting)
sudo nids-ipv6-config set-log-level DEBUG

# Normal operation
sudo nids-ipv6-config set-log-level INFO

# Warnings and errors only
sudo nids-ipv6-config set-log-level WARNING

# Errors only
sudo nids-ipv6-config set-log-level ERROR

# Critical errors only
sudo nids-ipv6-config set-log-level CRITICAL
```

Check logs:
```bash
sudo tail -f /var/log/nids/ipv6_config.log
```

Use:
- **DEBUG** - When troubleshooting issues
- **INFO** - Normal production use
- **ERROR** - When you only care about problems

### Packet Capture Filter

What traffic to capture. Uses BPF (Berkeley Packet Filter) syntax.

```bash
# All IPv6 traffic
sudo nids-ipv6-config set-pcap-filter "ip6"

# Only HTTPS (TCP port 443)
sudo nids-ipv6-config set-pcap-filter "tcp port 443"

# Only DNS (UDP port 53)
sudo nids-ipv6-config set-pcap-filter "udp port 53"

# TCP or UDP traffic
sudo nids-ipv6-config set-pcap-filter "tcp or udp"

# ICMP6 (IPv6 ping)
sudo nids-ipv6-config set-pcap-filter "icmpv6"

# Specific subnet
sudo nids-ipv6-config set-pcap-filter "dst 2001:db8::/32"
```

Common filters:
- `ip6` - All IPv6
- `tcp port 443` - HTTPS only
- `udp port 53` - DNS only
- `tcp` - All TCP traffic
- `udp` - All UDP traffic

### Alert Threshold

How many suspicious events before alerting (1-10000).

```bash
# Alert on 50 events
sudo nids-ipv6-config set-alert-threshold 50

# Alert on 100 events
sudo nids-ipv6-config set-alert-threshold 100

# Alert on 500 events
sudo nids-ipv6-config set-alert-threshold 500
```

Use:
- **Lower (10-50)** - High sensitivity for troubleshooting
- **Medium (100-200)** - Balanced for production
- **Higher (500+)** - Low sensitivity for noisy networks

### Statistics Interval

How often to generate performance stats (in seconds).

```bash
# Every 10 seconds (frequent)
sudo nids-ipv6-config set-stats-interval 10

# Every 60 seconds (default)
sudo nids-ipv6-config set-stats-interval 60

# Every 5 minutes
sudo nids-ipv6-config set-stats-interval 300
```

## Quick Configuration Profiles

### Development Environment

```bash
# Verbose for debugging
sudo nids-ipv6-config set-log-level DEBUG

# Listen locally
sudo nids-ipv6-config set-address ::1

# Custom port for testing
sudo nids-ipv6-config set-port 9000

# Sensitive alerts
sudo nids-ipv6-config set-alert-threshold 10

# Frequent stats
sudo nids-ipv6-config set-stats-interval 10
```

### Production Environment

```bash
# Standard logging
sudo nids-ipv6-config set-log-level INFO

# Listen on all interfaces
sudo nids-ipv6-config set-address ::

# Standard port
sudo nids-ipv6-config set-port 25826

# Higher alert threshold
sudo nids-ipv6-config set-alert-threshold 200

# Less frequent stats
sudo nids-ipv6-config set-stats-interval 300
```

### High-Traffic Network

```bash
# Normal logging
sudo nids-ipv6-config set-log-level INFO

# Listen on all interfaces
sudo nids-ipv6-config set-address ::

# Higher alert threshold to reduce noise
sudo nids-ipv6-config set-alert-threshold 500

# Less frequent stats to reduce overhead
sudo nids-ipv6-config set-stats-interval 600
```

### Compliance/Audit Mode

```bash
# Very detailed logging
sudo nids-ipv6-config set-log-level DEBUG

# Monitor all IPv6 traffic
sudo nids-ipv6-config set-pcap-filter "ip6"

# Sensitive alert threshold
sudo nids-ipv6-config set-alert-threshold 50

# Enable monitoring and rules
sudo nids-ipv6-config enable-monitoring
sudo nids-ipv6-config enable-rules
```

## View Configuration File

To see the raw JSON:

```bash
sudo cat /etc/nids/ipv6_config.json
```

Example output:
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

## Validation

Always validate after making changes:

```bash
sudo nids-ipv6-config validate
```

Good output:
```
✓ Configuration is valid
```

If validation fails, check the error message and see troubleshooting below.

## Troubleshooting Configuration

### Invalid IPv6 Address

```bash
# Wrong
sudo nids-ipv6-config set-address "not-an-address"

# Error: Invalid IPv6 address

# Correct
sudo nids-ipv6-config set-address ::
```

Valid IPv6 formats:
- `::` (all zeros)
- `::1` (loopback)
- `fe80::1` (with fe80 prefix)
- `2001:db8::1` (full notation)

### Port Out of Range

```bash
# Wrong
sudo nids-ipv6-config set-port 99999

# Error: Invalid port number

# Correct
sudo nids-ipv6-config set-port 9000
```

Valid ports: 1-65535

### Configuration Won't Apply

```bash
# Check if changes were saved
sudo nids-ipv6-config show

# Check logs for errors
sudo tail -20 /var/log/nids/ipv6_config.log

# Validate configuration
sudo nids-ipv6-config validate
```

### Settings Reset After Reboot

Configuration should persist. If it doesn't:

```bash
# Check file permissions
ls -la /etc/nids/ipv6_config.json

# Verify directory permissions
ls -la /etc/nids/

# Check logs
sudo tail -30 /var/log/nids/ipv6_config.log
```

## Backup & Restore

### Backup Current Settings

```bash
# Simple backup
sudo cp /etc/nids/ipv6_config.json /etc/nids/ipv6_config.json.backup

# Timestamped backup
sudo cp /etc/nids/ipv6_config.json /etc/nids/ipv6_config.json.$(date +%Y%m%d-%H%M%S)

# List backups
ls -la /etc/nids/ipv6_config.json*
```

### Restore Settings

```bash
# Restore from backup
sudo cp /etc/nids/ipv6_config.json.backup /etc/nids/ipv6_config.json

# Verify restoration
sudo nids-ipv6-config show
sudo nids-ipv6-config validate
```

## Common Workflows

### Change to Debug Mode and Back

```bash
# Current mode
sudo nids-ipv6-config show | grep logging_level

# Change to debug
sudo nids-ipv6-config set-log-level DEBUG

# Monitor logs
sudo tail -f /var/log/nids/ipv6_config.log

# When done, switch back
sudo nids-ipv6-config set-log-level INFO
```

### Configure for Specific Traffic

```bash
# Monitor HTTPS only
sudo nids-ipv6-config set-pcap-filter "tcp port 443"
sudo nids-ipv6-config enable-monitoring

# Monitor DNS
sudo nids-ipv6-config set-pcap-filter "udp port 53"

# Monitor everything again
sudo nids-ipv6-config set-pcap-filter "ip6"
```

### Test Configuration Changes

```bash
# Make a change
sudo nids-ipv6-config set-port 9000

# Verify it was applied
sudo nids-ipv6-config show

# Revert if needed
sudo nids-ipv6-config set-port 25826
```