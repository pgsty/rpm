Name:           ansible
Version:        2.16.14
Release:        1PIGSTY%{?dist}
Summary:        Meta package for Pigsty Ansible stack on EL10

License:        MIT
URL:            https://docs.ansible.com/
BuildArch:      noarch

Requires:       ansible-core
Requires:       ansible-collection-community-general
Requires:       ansible-collection-community-crypto
Requires:       ansible-collection-ansible-posix
Recommends:     python3-jmespath

%description
Meta package that pulls in ansible-core and required collections for Pigsty on EL10.
This package itself contains no files, only dependency information.

%prep
# nothing

%build
# nothing

%install
# nothing

%files
# no files

%changelog
* Sun Nov 23 2025 Ruohang Feng <rh@vonng.com> - 2.16.14-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
