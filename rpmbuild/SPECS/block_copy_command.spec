%define debug_package %{nil}
%global pname block_copy_command
%global sname block_copy_command
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 13 || 0%{?pgmajorversion} > 18
%{error:block_copy_command supports PostgreSQL 13-18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.5
Release:	1PIGSTY%{?dist}
Summary:	Block COPY commands cluster-wide with a ProcessUtility hook
License:	BSD-3-Clause
URL:		https://github.com/rustwizard/block_copy_command
Source0:	%{sname}-%{version}.tar.gz
#           repacked from upstream git tag https://github.com/rustwizard/block_copy_command/tree/v0.1.5

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	clang
Requires:	postgresql%{pgmajorversion}-server

%description
block_copy_command is a PostgreSQL security extension that intercepts COPY,
COPY FROM, and COPY PROGRAM via a ProcessUtility hook. It is intended to be
loaded through shared_preload_libraries and supports role-based blocking,
direction-specific rules, audit logging, and custom hints.

%prep
%setup -q -n %{sname}-%{version}

%build
cd %{_builddir}/%{sname}-%{version}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
cargo fetch
# pgrx 0.17.0 uses NonNull::from_mut(), which is newer than the EL9 Rust
# shipped in our validation container. Rewriting to NonNull::from(&mut ...)
# preserves semantics and keeps the extension buildable on EL9A.
PBOX="$(find "$HOME/.cargo/registry/src" -path '*/pgrx-0.17.0/src/palloc/pbox.rs' | head -n 1)"
test -n "$PBOX"
if ! grep -q 'NonNull::from(\&mut datum)' "$PBOX"; then \
    (cd "$(dirname "$PBOX")" && patch -p0 < %{_specdir}/patches/pgrx-0.17.0-pbox-nonnull.patch); \
fi
cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/lib
%{__mkdir_p} %{buildroot}%{pginstdir}/share/extension
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}
%{__mkdir_p} %{buildroot}%{_licensedir}/%{name}
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 %{_builddir}/%{sname}-%{version}/README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 %{_builddir}/%{sname}-%{version}/LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.md
%license %{_licensedir}/%{name}/LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.1.5-1PIGSTY
- Package upstream tag v0.1.5 for PostgreSQL 13-18
- Build with cargo-pgrx 0.17.0 and patch cached pgrx for EL9A Rust compatibility
