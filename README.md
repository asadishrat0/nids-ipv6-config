# NIDS IPv6 Configuration Application

## Overview

The NIDS IPv6 Configuration Application is a production-grade software package designed to manage Network Intrusion Detection System (NIDS) IPv6 settings across multiple Linux distributions. This application enables operators to configure IPv6 monitoring capabilities, manage traffic rules, and monitor system performance through a command-line interface.

**Supported Platforms:**
- Red Hat 9.6 (RPM)
- Ubuntu 22.04 LTS (DEB)

## Project Structure

```
nids-ipv6-config/
├── src/
│   └── nids_ipv6_config.py          # Main application
├── packaging/
│   └── nids-ipv6-config.spec        # RPM specification
├── config/
│   └── ipv6_config.json             # Default configuration
├── debian/
│   ├── control                      # DEB control file
│   ├── postinst                     # DEB post-install script
│   └── prerm                        # DEB pre-removal script
├── tests/
│   └── test_nids_config.py          # Unit tests
├── Jenkinsfile                      # CI/CD pipeline
├── README.md                        # This file
├── INSTALL.md                       # Installation guide
└── CONFIG.md                        # Configuration guide
```

## Features

- **IPv6 Configuration Management** - Enable/disable IPv6 monitoring
- **Port Management** - Configure listen ports (1-65535)
- **Address Configuration** - Set IPv6 listen addresses
- **Logging Control** - Multiple logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **Traffic Rules** - Enable/disable traffic rule enforcement
- **Monitoring** - Enable/disable packet monitoring
- **Alert Management** - Configure alert thresholds
- **PCAP Filtering** - Set packet capture filters
- **Configuration Persistence** - JSON-based configuration storage
- **Audit Logging** - Comprehensive audit trail in `/var/log/nids/`
- **Validation** - Built-in configuration validation

## Installation

### Quick Start - Ubuntu 22.04 LTS

```bash
# Install from DEB package
sudo apt-get update
sudo apt-get install ./nids-ipv6-config_1.0.0-1_all.deb

# Verify installation
nids-ipv6-config show
```

### Quick Start - Red Hat 9.6

```bash
# Install from RPM package
sudo yum install ./nids-ipv6-config-1.0.0-1.el9.noarch.rpm

# Verify installation
nids-ipv6-config show
```

For detailed installation instructions, see [INSTALL.md](INSTALL.md).

## Usage

### Show Current Configuration

```bash
sudo nids-ipv6-config show
```

### Enable IPv6 Monitoring

```bash
sudo nids-ipv6-config enable
```

### Disable IPv6 Monitoring

```bash
sudo nids-ipv6-config disable
```

### Configure IPv6 Address

```bash
sudo nids-ipv6-config set-address ::1
sudo nids-ipv6-config set-address fe80::1
```

### Configure Port

```bash
sudo nids-ipv6-config set-port 25826
```

### Set Logging Level

```bash
sudo nids-ipv6-config set-log-level DEBUG
sudo nids-ipv6-config set-log-level INFO
```

### Enable/Disable Traffic Rules

```bash
sudo nids-ipv6-config enable-rules
sudo nids-ipv6-config disable-rules
```

### Enable/Disable Monitoring

```bash
sudo nids-ipv6-config enable-monitoring
sudo nids-ipv6-config disable-monitoring
```

### Set PCAP Filter

```bash
sudo nids-ipv6-config set-pcap-filter "ip6"
sudo nids-ipv6-config set-pcap-filter "tcp port 443"
```

### Configure Alert Threshold

```bash
sudo nids-ipv6-config set-alert-threshold 100
```

### Set Statistics Interval

```bash
sudo nids-ipv6-config set-stats-interval 60
```

### Validate Configuration

```bash
sudo nids-ipv6-config validate
```

For detailed configuration options, see [CONFIG.md](CONFIG.md).

## Configuration File

Default configuration location: `/etc/nids/ipv6_config.json`

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

## Logging

Application logs are stored at: `/var/log/nids/ipv6_config.log`

Log levels include DEBUG, INFO, WARNING, ERROR, and CRITICAL. Adjust logging via:
```bash
sudo nids-ipv6-config set-log-level DEBUG
```

## Requirements

**System Requirements:**
- Python 3.9 or later
- Root/sudo privileges for configuration changes
- Minimum 100MB disk space
- Read/write access to `/etc/nids/` and `/var/log/nids/`

**Python Dependencies:**
- Built-in libraries only (standard library)
- No external Python packages required

## Build & Package

### Build RPM

```bash
rpmbuild -bb packaging/nids-ipv6-config.spec
```

### Build DEB

```bash
dpkg-deb --build debian/
```

### Jenkins Pipeline

Automated builds are managed through Jenkinsfile:
- Syntax validation
- Unit tests
- Package creation (RPM & DEB)
- Package validation
- Integration tests

## Troubleshooting

### Permission Denied

Most commands require root privileges. Use `sudo`:
```bash
sudo nids-ipv6-config show
```

### Configuration File Not Found

After installation, verify the config file exists:
```bash
ls -la /etc/nids/ipv6_config.json
```

### Invalid IPv6 Address

Validate your IPv6 address format:
```bash
# Valid addresses
::1
::
fe80::1
2001:db8::1
```

### Service Not Starting

Check logs for errors:
```bash
sudo tail -f /var/log/nids/ipv6_config.log
```

### Validation Fails

Run validation with detailed output:
```bash
sudo nids-ipv6-config validate
```

## Contributing

1. Follow PEP 8 style guidelines
2. Include unit tests for new features
3. Update documentation with changes
4. Test on both Ubuntu 22.04 and Red Hat 9.6

## Security Considerations

- Configuration files are readable only by root (mode 0640)
- Audit trail maintained in system logs
- Input validation on all configuration parameters
- IPv6 address format validation
- Port range validation (1-65535)

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions, please contact: devops@example.com

## Changelog

### Version 1.0.0 (November 2025)
- Initial release
- Full IPv6 configuration support
- RPM and DEB packaging
- Comprehensive logging
- Jenkins CI/CD integration