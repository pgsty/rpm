%define debug_package %{nil}
%global pname pg_rrf
%global sname pg_rrf
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 17
%{error:pg_rrf supports PostgreSQL 14-17}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.3
Release:	1PIGSTY%{?dist}
Summary:	Reciprocal Rank Fusion functions for hybrid search in PostgreSQL
License:	MIT
URL:		https://github.com/yuiseki/pg_rrf
Source0:	%{sname}-%{version}.tar.gz
#           repacked from upstream release/tag https://github.com/yuiseki/pg_rrf/releases/tag/v0.0.3

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	clang
Requires:	postgresql%{pgmajorversion}-server

%description
pg_rrf provides Reciprocal Rank Fusion helper functions for hybrid search and
rank-score fusion inside PostgreSQL. It exposes scalar and set-returning
functions for combining ranked ID lists directly in SQL.

%prep
%setup -q -n %{sname}-%{version}
find . -type f -name '._*' -delete
patch -p1 < %{_specdir}/patches/pg_rrf-0.0.3-pgrx-0.17.0.patch

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
cp -a %{_builddir}/%{sname}-%{version}/%{pname}--*--*.sql %{buildroot}%{pginstdir}/share/extension/
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
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.0.3-1PIGSTY
- Package upstream release v0.0.3 for PostgreSQL 14-17
- Build with cargo-pgrx 0.17.0 after patching the upstream Cargo manifest
