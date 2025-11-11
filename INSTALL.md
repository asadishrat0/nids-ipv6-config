# NIDS IPv6 Configuration Application - Installation Guide

## Prerequisites

### System Requirements

| Requirement | Details |
|---|---|
| **OS** | Red Hat 9.6 or Ubuntu 22.04 LTS |
| **Python** | 3.9 or later |
| **RAM** | Minimum 512MB |
| **Disk Space** | Minimum 100MB |
| **Permissions** | Root/sudo access required |

### Verify Prerequisites

```bash
# Check Python version
python3 --version

# Check if you have sudo access
sudo echo "Sudo access verified"

# Check available disk space
df -h /
```

## Installation on Ubuntu 22.04 LTS

### Method 1: Using APT (Recommended)

If added to APT repository:

```bash
# Update package index
sudo apt-get update

# Install the package
sudo apt-get install nids-ipv6-config

# Verify installation
nids-ipv6-config --help
```

### Method 2: Manual DEB Installation

```bash
# Download the DEB package
wget https://repo.example.com/nids-ipv6-config_1.0.0-1_all.deb

# Install the package
sudo apt-get install ./nids-ipv6-config_1.0.0-1_all.deb

# Verify installation
nids-ipv6-config show

# Check logs
tail -f /var/log/nids/ipv6_config.log
```

### Method 3: From Source (Development)

```bash
# Clone the repository
git clone https://github.com/your-org/nids-ipv6-config.git
cd nids-ipv6-config

# Install Python dependencies (if any)
pip3 install -r requirements.txt

# Install application
sudo python3 setup.py install

# Or create DEB package
dpkg-deb --build debian/
sudo apt-get install ./nids-ipv6-config_1.0.0-1_all.deb
```

### Post-Installation Setup (Ubuntu)

```bash
# Create configuration directory
sudo mkdir -p /etc/nids
sudo mkdir -p /var/log/nids

# Set proper permissions
sudo chmod 755 /etc/nids
sudo chmod 755 /var/log/nids

# Initialize configuration
sudo nids-ipv6-config show

# Verify installation
sudo nids-ipv6-config validate
```

## Installation on Red Hat 9.6

### Method 1: Using YUM (Recommended)

If added to YUM repository:

```bash
# Update package index
sudo yum update -y

# Install the package
sudo yum install nids-ipv6-config

# Verify installation
nids-ipv6-config --help
```

### Method 2: Manual RPM Installation

```bash
# Download the RPM package
wget https://repo.example.com/nids-ipv6-config-1.0.0-1.el9.noarch.rpm

# Install the package
sudo yum install ./nids-ipv6-config-1.0.0-1.el9.noarch.rpm

# Verify installation
nids-ipv6-config show

# Check logs
tail -f /var/log/nids/ipv6_config.log
```

### Method 3: From Source (Development)

```bash
# Install build dependencies
sudo yum install rpm-build python3-devel -y

# Clone the repository
git clone https://github.com/your-org/nids-ipv6-config.git
cd nids-ipv6-config

# Build RPM package
rpmbuild -bb packaging/nids-ipv6-config.spec

# Install the RPM
sudo yum install ~/rpmbuild/RPMS/noarch/nids-ipv6-config-1.0.0-1.el9.noarch.rpm
```

### Post-Installation Setup (Red Hat)

```bash
# Create configuration directory
sudo mkdir -p /etc/nids
sudo mkdir -p /var/log/nids

# Set proper permissions
sudo chmod 755 /etc/nids
sudo chmod 755 /var/log/nids

# Initialize configuration
sudo nids-ipv6-config show

# Verify installation
sudo nids-ipv6-config validate
```

## Verification

### Check Installation Success

```bash
# Verify binary location
which nids-ipv6-config

# Verify file permissions
ls -la /usr/bin/nids-ipv6-config

# Verify configuration directory
ls -la /etc/nids/

# Verify log directory
ls -la /var/log/nids/
```

### Run Tests

```bash
# Show current configuration
sudo nids-ipv6-config show

# Validate configuration
sudo nids-ipv6-config validate

# Test enable/disable
sudo nids-ipv6-config enable
sudo nids-ipv6-config disable

# Test address configuration
sudo nids-ipv6-config set-address ::1
sudo nids-ipv6-config show
```

### Expected Output

```bash
$ sudo nids-ipv6-config show

=== NIDS IPv6 Configuration ===
ipv6_enabled................................ True
listen_address........................... ::
listen_port............................. 25826
monitoring_enabled...................... True
traffic_rules_enabled................... True
logging_level............................ INFO
max_packet_size....................... 65535
pcap_filter............................. ip6
alert_threshold......................... 100
stats_interval........................... 60
===================================
```

## Upgrading

### Ubuntu 22.04 LTS

```bash
# Download new version
wget https://repo.example.com/nids-ipv6-config_1.1.0-1_all.deb

# Upgrade package
sudo apt-get install ./nids-ipv6-config_1.1.0-1_all.deb

# Verify upgrade
nids-ipv6-config show
```

### Red Hat 9.6

```bash
# Download new version
wget https://repo.example.com/nids-ipv6-config-1.1.0-1.el9.noarch.rpm

# Upgrade package
sudo yum upgrade ./nids-ipv6-config-1.1.0-1.el9.noarch.rpm

# Verify upgrade
nids-ipv6-config show
```

## Uninstallation

### Ubuntu 22.04 LTS

```bash
# Remove package
sudo apt-get remove nids-ipv6-config

# Remove configuration (optional)
sudo rm -rf /etc/nids
sudo rm -rf /var/log/nids
```

### Red Hat 9.6

```bash
# Remove package
sudo yum remove nids-ipv6-config

# Remove configuration (optional)
sudo rm -rf /etc/nids
sudo rm -rf /var/log/nids
```

## Troubleshooting

### Issue: "Command not found"

```bash
# Verify PATH includes /usr/bin
echo $PATH

# Try full path
/usr/bin/nids-ipv6-config show
```

### Issue: "Permission denied"

```bash
# All commands require sudo
sudo nids-ipv6-config show

# Check file permissions
ls -la /usr/bin/nids-ipv6-config
```

### Issue: Configuration file missing

```bash
# Check if file exists
ls -la /etc/nids/ipv6_config.json

# Create from example
sudo cp /etc/nids/ipv6_config.json.example /etc/nids/ipv6_config.json
sudo chmod 640 /etc/nids/ipv6_config.json
```

### Issue: Cannot write to log directory

```bash
# Check directory permissions
ls -la /var/log/nids/

# Fix permissions
sudo chmod 755 /var/log/nids/
sudo chown root:root /var/log/nids/
```

### Issue: Application crashes

```bash
# Check logs for errors
sudo tail -100 /var/log/nids/ipv6_config.log

# Run validation
sudo nids-ipv6-config validate

# Try manual operation
sudo python3 /usr/bin/nids-ipv6-config show
```

## Integration with Existing Systems

### Adding to APT Repository

1. Place DEB in repository directory
2. Update Packages index
3. Sign with GPG key
4. Update apt sources

### Adding to YUM Repository

1. Place RPM in repository directory
2. Run `createrepo`
3. Sign with GPG key
4. Update yum configuration

### CI/CD Integration

See Jenkinsfile for automated build and deployment pipeline.

## Next Steps

1. Read [CONFIG.md](CONFIG.md) for configuration options
2. Review [README.md](README.md) for usage examples
3. Check logs at `/var/log/nids/ipv6_config.log`
4. Configure IPv6 settings for your environment

## Support

For installation issues or questions, contact: devops@example.com