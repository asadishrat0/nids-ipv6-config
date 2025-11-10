Name:           nids-ipv6-config
Version:        1.0.0
Release:        1%{?dist}
Summary:        Network Intrusion Detection System IPv6 Configuration Application

License:        MIT
URL:            https://github.com/your-org/nids-ipv6-config
Source0:        nids-ipv6-config-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
Requires:       python3 >= 3.9

%description
A configuration application for managing Network Intrusion Detection System (NIDS) IPv6 settings
on Red Hat 9.6 and Ubuntu 22.04 LTS systems. Provides command-line interface for IPv6 mode
capability configuration.

%prep
%autosetup

%build
# No compilation needed for Python application
echo "Build stage - Python application"

%install
# Create directory structure
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/etc/nids
mkdir -p %{buildroot}/var/log/nids
mkdir -p %{buildroot}/usr/share/doc/nids-ipv6-config
mkdir -p %{buildroot}/usr/share/man/man1

# Install main application
install -m 0755 src/nids_ipv6_config.py %{buildroot}/usr/bin/nids-ipv6-config

# Install configuration file
install -m 0640 config/ipv6_config.json %{buildroot}/etc/nids/ipv6_config.json.example

# Install documentation
install -m 0644 README.md %{buildroot}/usr/share/doc/nids-ipv6-config/
install -m 0644 INSTALL.md %{buildroot}/usr/share/doc/nids-ipv6-config/
install -m 0644 CONFIG.md %{buildroot}/usr/share/doc/nids-ipv6-config/

%files
%defattr(-,root,root,-)
/usr/bin/nids-ipv6-config
%config(noreplace) /etc/nids/ipv6_config.json.example
%dir /etc/nids
%dir /var/log/nids
/usr/share/doc/nids-ipv6-config/README.md
/usr/share/doc/nids-ipv6-config/INSTALL.md
/usr/share/doc/nids-ipv6-config/CONFIG.md

%post
# Create initial config if it doesn't exist
if [ ! -f /etc/nids/ipv6_config.json ]; then
    cp /etc/nids/ipv6_config.json.example /etc/nids/ipv6_config.json
    chmod 0640 /etc/nids/ipv6_config.json
fi

# Create log directory if needed
mkdir -p /var/log/nids
chmod 0755 /var/log/nids

# Verify installation
/usr/bin/nids-ipv6-config validate

%preun
# Cleanup on uninstall
echo "Uninstalling NIDS IPv6 Configuration Application"

%changelog
* Mon Nov 10 2025 DevOps Team <devops@example.com> - 1.0.0-1
- Initial release of NIDS IPv6 Configuration Application
- Support for Red Hat 9.6
- IPv6 configuration and validation
- Automated logging and configuration management