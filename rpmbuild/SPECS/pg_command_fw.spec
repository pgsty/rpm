%define debug_package %{nil}
%global pname pg_command_fw
%global sname pg_command_fw
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 15
%{error:pg_command_fw only supports PostgreSQL 15+}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.0
Release:	1PIGSTY%{?dist}
Summary:	DDL and utility command firewall for PostgreSQL
License:	BSD-3-Clause
URL:		https://github.com/rustwizard/pg_command_fw
Source0:	%{sname}-%{version}.zip
#           https://api.pgxn.org/dist/pg_command_fw/0.1.0/pg_command_fw-0.1.0.zip

# cargo/rust/cargo-pgrx/rustfmt are provisioned manually on builders via
# `pig build rust` and `pig build pgrx -v 0.17.0`, so they are intentionally
# not declared as BuildRequires here.
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	clang
BuildRequires:	unzip
Requires:	postgresql%{pgmajorversion}-server

%description
pg_command_fw is a PostgreSQL extension that intercepts and blocks selected
DDL, utility commands, and dangerous built-in functions through configurable
hooks.

%prep
%{__rm} -rf %{_builddir}/%{sname}-%{version}
cd %{_builddir}
unzip -q %{SOURCE0}

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
cargo pgrx package --pg-config %{pginstdir}/bin/pg_config

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

%changelog
* Mon Apr 06 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Restrict builds to PostgreSQL 15+ and initialize cargo-pgrx with the active pgmajorversion

* Sun Apr 05 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
