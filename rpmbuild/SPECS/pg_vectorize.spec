%define debug_package %{nil}
%global pname vectorize
%global sname pg_vectorize
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.26.1
Release:	1PIGSTY%{?dist}
Summary:	The simplest way to orchestrate vector search on Postgres
License:	PostgreSQL
URL:		https://github.com/ChuckHend/pg_vectorize
SOURCE0:    pg_vectorize-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server pgmq_%{pgmajorversion} >= 1.1.1 pgvector_%{pgmajorversion} >= 0.7.0 pg_cron_%{pgmajorversion}
Recommends: pg_cron_%{pgmajorversion}

%description
A Postgres extension that automates the transformation and orchestration of text to embeddings and provides hooks into the most popular LLMs.
This allows you to do vector search and build LLM applications on existing data with as little as two function calls.

%prep
%setup -q -n %{sname}-%{version}

%build
cd %{_builddir}/%{sname}-%{version}/extension
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
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/%{sname}-%{version}/extension/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/extension/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/extension/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.26.1-1PIGSTY
- https://github.com/ChuckHend/pg_vectorize/releases/tag/v0.26.1
- Build with cargo-pgrx 0.17.0 and patch cached pgrx for EL9A Rust compatibility
* Tue Nov 18 2025 Vonng <rh@vonng.com> - 0.26.0-1PIGSTY
* Mon Oct 27 2025 Vonng <rh@vonng.com> - 0.25.0-1PIGSTY
* Thu May 22 2025 Vonng <rh@vonng.com> - 0.22.2-1PIGSTY
* Sat Apr 05 2025 Vonng <rh@vonng.com> - 0.22.1-1PIGSTY
* Tue Feb 11 2025 Vonng <rh@vonng.com> - 0.21.1-1PIGSTY
* Wed Oct 30 2024 Vonng <rh@vonng.com> - 0.20.0-1PIGSTY
* Mon Oct 14 2024 Vonng <rh@vonng.com> - 0.18.3-1PIGSTY
* Thu Jul 18 2024 Vonng <rh@vonng.com> - 0.17.0-1PIGSTY
* Sat Jun 29 2024 Vonng <rh@vonng.com> - 0.16.0-1PIGSTY
* Sun May 05 2024 Vonng <rh@vonng.com> - 0.15.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
