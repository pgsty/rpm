%global pname wrappers
%global sname wrappers
%global srcdir wrappers-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.6.3
Release:	1PGSTY%{?dist}
Summary:	Postgres Foreign Data Wrappers by Supabase
License:	Apache-2.0
URL:		https://github.com/supabase/wrappers
Source0:    wrappers-%{version}.tar.gz
Patch0:     wrappers-0.6.3.patch
#           https://github.com/supabase/wrappers/archive/refs/tags/v0.6.3.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	clang
%if 0%{?rhel} == 8
BuildRequires:	file
%endif
Requires:	postgresql%{pgmajorversion}-server

%description
Wrappers is a development framework for Postgres Foreign Data Wrappers (FDW), written in Rust.
Its goal is to make Postgres FDW development easier while keeping Rust's
strong performance, type safety, and modern tooling. The project bundles
and supports a growing set of FDWs for external services and data platforms.

%prep
%setup -q -n %{srcdir}
# Upstream supplies pgrx 0.19.2 and ethnum 1.5.3; retain the SQL ordering fix.
patch --batch --fuzz=0 -p1 < %{PATCH0}

%build
%set_build_flags
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
# Fat LTO over all FDWs exceeds the pilot builder's memory budget.
export CARGO_PROFILE_RELEASE_LTO="${CARGO_PROFILE_RELEASE_LTO:-thin}"
cd %{_builddir}/%{srcdir}/%{pname}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.19.2
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
cargo fetch --locked
LOCK_FILE=../Cargo.lock
LOCK_SHA256=$(sha256sum "$LOCK_FILE" | awk '{print $1}')

export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion},all_fdws --pg-config %{pginstdir}/bin/pg_config
test "$LOCK_SHA256" = "$(sha256sum "$LOCK_FILE" | awk '{print $1}')" || {
	echo "Cargo.lock changed during package" >&2
	exit 1
}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
PACKAGE_TARGET="${CARGO_TARGET_DIR:-%{_builddir}/%{srcdir}/target}"
cp -a "$PACKAGE_TARGET/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}-%{version}.so"       %{buildroot}%{pginstdir}/lib/
cp -a "$PACKAGE_TARGET/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control" %{buildroot}%{pginstdir}/share/extension/
cp -a "$PACKAGE_TARGET/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/"%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%if 0%{?rhel} == 8
# EL8 file defaults to 32768 ELF sections; all_fdws exceeds that limit.
# Let find-debuginfo recognize the unstripped library without removing notes
# or DWARF. The file 5.33 section limit is a uint16_t, so 65536 wraps to zero.
mkdir -p %{_builddir}/%{srcdir}/.rpm-tools
cat > %{_builddir}/%{srcdir}/.rpm-tools/file <<'EOF'
#!/bin/sh
exec /usr/bin/file -P elf_shnum=65535 "$@"
EOF
chmod 755 %{_builddir}/%{srcdir}/.rpm-tools/file
export PATH=%{_builddir}/%{srcdir}/.rpm-tools:$PATH
%endif

%files
%license LICENSE
%{pginstdir}/lib/%{pname}-%{version}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Sun Sep 20 2026 Vonng <rh@vonng.com> - 0.6.3-1PGSTY
- Raise the EL8 file section limit so complete debug packages are extracted

* Sat Sep 19 2026 Vonng <rh@vonng.com> - 0.6.3-1PGSTY
- Update to 0.6.3
- Include the upstream license in the binary package

* Sun Sep 06 2026 Vonng <rh@vonng.com> - 0.6.2-1PGSTY
- Build with pgrx 0.19.2 from the updated source archive and locked dependencies
- Declare clang as a build dependency for pgrx bindgen

* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.6.2-1PIGSTY
- Update to upstream 0.6.2 and migrate both pgrx workspace crates to 0.19.1
- Preserve the packaging error-report compatibility fix in the versioned patch

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.6.1-1PIGSTY
- https://github.com/supabase/wrappers/releases/tag/v0.6.1
- Patch Cargo metadata to build with cargo-pgrx 0.18.1

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.6.0-1PIGSTY
- https://github.com/supabase/wrappers/releases/tag/v0.6.0
- Build with cargo-pgrx 0.17.0 and patch cached pgrx for EL9A Rust compatibility
* Mon Dec 15 2025 Vonng <rh@vonng.com> - 0.5.7-1PIGSTY
* Wed Oct 29 2025 Vonng <rh@vonng.com> - 0.5.6-1PIGSTY
* Mon Oct 27 2025 Vonng <rh@vonng.com> - 0.5.5-1PIGSTY
* Thu Sep 04 2025 Vonng <rh@vonng.com> - 0.5.4-1PIGSTY
* Wed Jul 23 2025 Vonng <rh@vonng.com> - 0.5.3-1PIGSTY
* Thu May 22 2025 Vonng <rh@vonng.com> - 0.5.0-1PIGSTY
* Wed May 07 2025 Vonng <rh@vonng.com> - 0.4.6-1PIGSTY
* Thu Mar 20 2025 Vonng <rh@vonng.com> - 0.4.5-1PIGSTY
* Wed Jan 08 2025 Vonng <rh@vonng.com> - 0.4.4-1PIGSTY
* Thu Oct 17 2024 Vonng <rh@vonng.com> - 0.4.3-1PIGSTY
* Mon Oct 14 2024 Vonng <rh@vonng.com> - 0.4.2-1PIGSTY
* Thu Jul 18 2024 Vonng <rh@vonng.com> - 0.4.1-1PIGSTY
* Sun May 05 2024 Vonng <rh@vonng.com> - 0.3.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
