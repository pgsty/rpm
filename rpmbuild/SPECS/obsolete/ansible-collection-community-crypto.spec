%if 0%{?rhel}
%bcond_with tests
%else
%bcond_without tests
%endif

%if 0%{?rhel} && 0%{?rhel} < 10
%{error:ansible-collection-community-crypto requires ansible-packaging from EL10}
%endif

Name:           ansible-collection-community-crypto
Version:        2.15.0
Release:        2PIGSTY%{?dist}
Summary:        The community.crypto collection for Ansible

# See the LICENSES directory and the summary in the README
License:        GPL-3.0-or-later AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND PSF-2.0
URL:            https://github.com/ansible-collections/community.crypto
Source:         https://github.com/ansible-collections/community.crypto/archive/%{version}/community.crypto-%{version}.tar.gz
# build_ignore development files, tests, and docs
Patch:          build_ignore.patch

BuildArch:      noarch

BuildRequires:  ansible-packaging
%if %{with tests}
BuildRequires:  ansible-packaging-tests
BuildRequires:  pyproject-rpm-macros
%endif

%description
%{summary}.


%prep
%autosetup -p1 -n community.crypto-%{version}
find -type f ! -executable -name '*.py' -print -exec sed -i -e '1{\@^#!.*@d}' '{}' +


%if %{with tests}
%generate_buildrequires
%pyproject_buildrequires -N tests/unit/requirements.txt
%endif


%build
%ansible_collection_build


%install
%ansible_collection_install


%check
%if %{with tests}
%ansible_test_unit
%endif


%files -f %{ansible_collection_filelist}
%license COPYING LICENSES .reuse/*
%doc README.md CHANGELOG.rst* docs/docsite/rst/


%changelog
* Tue Jul 28 2026 Vonng <rh@vonng.com> - 2.15.0-2PIGSTY
- Keep tests disabled on EL with rpm 4.14 compatible bcond syntax
- Avoid requiring ansible-packaging macros while parsing package metadata
- Restrict the package to EL10 where ansible-packaging is available

* Sun Nov 23 2025 Maxwell G <maxwell@gtmx.me> - 2.15.0-1PIGSTY
- Update to 2.15.0. Fixes rhbz#2231669.

* Sun Aug 13 2023 Maxwell G <maxwell@gtmx.me> - 2.15.0-1
- Update to 2.15.0. Fixes rhbz#2231669.

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Maxwell G <maxwell@gtmx.me> - 2.14.1-1
- Initial package. Fixes rhbz#2222120.
