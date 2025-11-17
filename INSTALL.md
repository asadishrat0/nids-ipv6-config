# Installation Guide

## Before You Start

Make sure your system meets these requirements:

- **OS:** Ubuntu 22.04 LTS or Red Hat 9.6
- **Python:** 3.9 or later (usually pre-installed)
- **Access:** Root or sudo privileges
- **Disk:** ~100MB free space in `/`

Check your system:

```bash
# Check OS version
cat /etc/os-release | grep "VERSION_ID"

# Check Python
python3 --version

# Check disk space
df -h /
```

## Installation on Ubuntu 22.04

### Quick Install

```bash
# Download and install
sudo apt-get update
sudo apt-get install ./nids-ipv6-config_1.0.0-1_all.deb

# Verify installation
sudo nids-ipv6-config show
```

### What Gets Installed

- Binary: `/usr/bin/nids-ipv6-config`
- Config: `/etc/nids/ipv6_config.json`
- Logs: `/var/log/nids/ipv6_config.log`

### Troubleshooting Ubuntu Install

**"File not found" error:**
```bash
# Make sure you're in the directory with the .deb file
ls *.deb

# Try with full path
sudo apt-get install /full/path/to/nids-ipv6-config_1.0.0-1_all.deb
```

**"Permission denied":**
```bash
# Always use sudo
sudo apt-get install ./nids-ipv6-config_1.0.0-1_all.deb
```

**Installation hangs:**
```bash
# Try force package configuration
sudo dpkg --configure -a
sudo apt-get install -f
```

## Installation on Red Hat 9.6

### Quick Install

```bash
# Install directly
sudo yum install ./nids-ipv6-config-1.0.0-1.el9.noarch.rpm

# Verify installation
sudo nids-ipv6-config show
```

### What Gets Installed

- Binary: `/usr/bin/nids-ipv6-config`
- Config: `/etc/nids/ipv6_config.json`
- Logs: `/var/log/nids/ipv6_config.log`

### Troubleshooting Red Hat Install

**"File not found" error:**
```bash
# Make sure you're in the directory with the .rpm file
ls *.rpm

# Try with full path
sudo yum install /full/path/to/nids-ipv6-config-1.0.0-1.el9.noarch.rpm
```

**RPM conflicts:**
```bash
# Check if already installed
rpm -qa | grep nids

# Remove old version
sudo yum remove nids-ipv6-config

# Install new version
sudo yum install ./nids-ipv6-config-1.0.0-1.el9.noarch.rpm
```

## Post-Installation

After installation on either system:

```bash
# Show current configuration
sudo nids-ipv6-config show

# Validate configuration
sudo nids-ipv6-config validate

# Check logs
sudo tail -20 /var/log/nids/ipv6_config.log
```

Expected output from `show`:
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

If you see this, installation was successful!

## Verify Installation

### Test the Application

```bash
# Get help
sudo nids-ipv6-config --help

# Show config
sudo nids-ipv6-config show

# Validate config
sudo nids-ipv6-config validate

# Try changing a setting
sudo nids-ipv6-config set-log-level DEBUG
sudo nids-ipv6-config show
sudo nids-ipv6-config set-log-level INFO
```

### Check File Permissions

```bash
# Check binary
ls -la /usr/bin/nids-ipv6-config

# Check config directory
ls -la /etc/nids/

# Check config file
ls -la /etc/nids/ipv6_config.json

# Check log directory
ls -la /var/log/nids/
```

Everything should be owned by root and readable.

## Upgrade

### From Older Version to 1.0.0

**Ubuntu:**
```bash
# Backup current config
sudo cp /etc/nids/ipv6_config.json /etc/nids/ipv6_config.json.old

# Upgrade
sudo apt-get install ./nids-ipv6-config_1.0.0-1_all.deb

# Verify
sudo nids-ipv6-config show
```

**Red Hat:**
```bash
# Backup current config
sudo cp /etc/nids/ipv6_config.json /etc/nids/ipv6_config.json.old

# Upgrade
sudo yum upgrade ./nids-ipv6-config-1.0.0-1.el9.noarch.rpm

# Verify
sudo nids-ipv6-config show
```

## Uninstall

### Ubuntu

```bash
# Remove package
sudo apt-get remove nids-ipv6-config

# Optional: Remove all configuration
sudo rm -rf /etc/nids
sudo rm -rf /var/log/nids
```

### Red Hat

```bash
# Remove package
sudo yum remove nids-ipv6-config

# Optional: Remove all configuration
sudo rm -rf /etc/nids
sudo rm -rf /var/log/nids
```

## Backup Before Changes

Always backup your configuration:

```bash
# Simple backup
sudo cp /etc/nids/ipv6_config.json /etc/nids/ipv6_config.json.backup

# Backup with timestamp
sudo cp /etc/nids/ipv6_config.json /etc/nids/ipv6_config.json.$(date +%Y%m%d)
```

## Getting Help

If something goes wrong:

1. **Check logs:**
   ```bash
   sudo tail -50 /var/log/nids/ipv6_config.log
   ```

2. **Validate config:**
   ```bash
   sudo nids-ipv6-config validate
   ```

3. **Check file permissions:**
   ```bash
   ls -la /etc/nids/
   ls -la /var/log/nids/
   ```

4. **Try re-installing:**
   ```bash
   sudo apt-get remove nids-ipv6-config
   sudo apt-get install ./nids-ipv6-config_1.0.0-1_all.deb
   ```