%global pname pg_tiktoken
%global sname pg_tiktoken
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global snapshot_date 20260825
%global snapshot_commit 99cb61d1f64b8c4aeb2fe7c5f7839fba54a7ccbf
%global snapshot_short 99cb61d
%global source_version 0.0.1+git%{snapshot_date}.%{snapshot_short}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_tiktoken only supports PostgreSQL 14 through 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.1
Release:	5.git%{snapshot_date}.%{snapshot_short}PGSTY%{?dist}
Summary:	OpenAI tiktoken tokenizer for postgres
License:	Apache-2.0
URL:		https://github.com/kelvich/pg_tiktoken
Source0:	%{sname}-%{source_version}.tar.gz
Patch0:		pg-tiktoken-0.0.1+git20260825.99cb61d.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	cargo clang git rust rustfmt
Requires:	postgresql%{pgmajorversion}-server

%description
Postgres extension that does input tokenization using OpenAI's tiktoken.

%prep
%setup -q -n %{sname}-%{source_version}
patch -p1 --fuzz=0 < %{PATCH0}

%build
export CARGO_PROFILE_RELEASE_DEBUG="${CARGO_PROFILE_RELEASE_DEBUG:-2}"
export CARGO_PROFILE_RELEASE_STRIP="${CARGO_PROFILE_RELEASE_STRIP:-none}"
cd %{_builddir}/%{sname}-%{source_version}
export PATH=%{pginstdir}/bin:$HOME/.cargo/bin:$PATH

PGRX_VERSION=0.19.2
CURRENT_PGRX=$(cargo pgrx --version 2>/dev/null | awk '{print $2}')
if [ "$CURRENT_PGRX" != "$PGRX_VERSION" ]; then
	echo "cargo-pgrx $PGRX_VERSION is required; run pig build pgrx -v $PGRX_VERSION before building" >&2
	exit 1
fi
cargo pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config --no-run
LOCK_BEFORE=$(sha256sum Cargo.lock | awk '{print $1}')
CARGO_NET_GIT_FETCH_WITH_CLI=true cargo fetch --locked
export RUSTFLAGS="${RUSTFLAGS:-} -C link-arg=-Wl,--no-gc-sections"
CARGO_NET_OFFLINE=true CARGO_NET_GIT_FETCH_WITH_CLI=true cargo pgrx package -v --no-default-features --features pg%{pgmajorversion} --pg-config %{pginstdir}/bin/pg_config
LOCK_AFTER=$(sha256sum Cargo.lock | awk '{print $1}')
if [ "$LOCK_BEFORE" != "$LOCK_AFTER" ]; then
	echo "Cargo.lock changed during cargo pgrx package" >&2
	exit 1
fi

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/%{sname}-%{source_version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{source_version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{source_version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Tue Sep 01 2026 Vonng <rh@vonng.com> - 0.0.1-5.git20260825.99cb61dPGSTY
- Package upstream main snapshot 99cb61d while keeping extension version 0.0.1
- Build PostgreSQL 14 through 18 with cargo-pgrx/pgrx 0.19.2
- Lock tiktoken-rs at 90e77bdd and reject dependency lock rewrites

* Fri Jul 17 2026 Vonng <rh@vonng.com> - 0.0.1-4PIGSTY
- Migrate the direct-on-pristine source patch and dependency graph to pgrx 0.19.1
- Add a fixed Cargo.lock for the upstream git dependency, build offline after locked fetch, and reject lock rewrites

* Mon Jun 15 2026 Vonng <rh@vonng.com> - 0.0.1-3PIGSTY
- Build with cargo-pgrx 0.18.1 and explicit pgNN features
- Use the shared pgrx 0.18.1 source patch from DEB packaging

* Sat Oct 25 2025 Vonng <rh@vonng.com> - 0.0.1-2PIGSTY
* Sun May 05 2024 Vonng <rh@vonng.com> - 0.0.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
