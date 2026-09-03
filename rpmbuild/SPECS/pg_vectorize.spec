%global pname vectorize
%global sname pg_vectorize
%global srcdir %{sname}-%{version}
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_vectorize supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.27.0
Release:	1PGSTY%{?dist}
Summary:	The simplest way to orchestrate vector search on Postgres
License:	PostgreSQL
URL:		https://github.com/ChuckHend/pg_vectorize
Source0:	pg_vectorize-%{version}.tar.gz
Patch0:		pg-vectorize-0.27.0.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang rust rustfmt
Requires:	postgresql%{pgmajorversion}-server pgmq_%{pgmajorversion} >= 1.1.1 pgvector_%{pgmajorversion} >= 0.7.0 pg_cron_%{pgmajorversion}
Recommends: pg_cron_%{pgmajorversion}

%description
A Postgres extension that automates the transformation and orchestration of text to embeddings and provides hooks into the most popular LLMs.
This allows you to do vector search and build LLM applications on existing data with as little as two function calls.

%prep
%setup -q -n %{srcdir}
patch -p1 --forward -f < %{PATCH0}

%build
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
cd %{_builddir}/%{srcdir}/extension
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.19.2
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
LOCK_BEFORE=$(sha256sum Cargo.lock | cut -d ' ' -f1)
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
cargo fetch --locked

export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
%if 0%{?rhel} >= 10
# aws-lc-sys 0.42 deliberately ignores CFLAGS for its executable compiler
# probe, but still inherits the EL10 hardened LDFLAGS that enable PIE.
export LDFLAGS="${LDFLAGS:-} -fPIE"
%endif
CARGO_NET_OFFLINE=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
LOCK_AFTER=$(sha256sum Cargo.lock | cut -d ' ' -f1)
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ]; then
	echo "Cargo.lock changed during cargo pgrx package" >&2
	exit 1
fi

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/%{srcdir}/extension/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{srcdir}/extension/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{srcdir}/extension/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Wed Sep 02 2026 Vonng <rh@vonng.com> - 0.27.0-1PGSTY
- Update the source package to upstream release 0.27.0
- Build PostgreSQL 14 through 18 with pgrx and cargo-pgrx 0.19.2
- Retain upstream SQL extension version 0.23.0 and a separate extension lock

* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.26.2-2PIGSTY
- Build the extension crate with cargo-pgrx 0.19.1 and a locked dependency graph
- Preserve the PG18 background-worker build and linker metadata retention flag

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.26.2-1PIGSTY
- Bump to 0.26.2 and patch Cargo metadata to pgrx 0.18.1

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
