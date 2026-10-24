%global _build_id_links none
%global pname provsql
%global sname provsql
%global pginstdir /usr/pgsql-%{pgmajorversion}
%{!?llvm:%global llvm 1}
%if %llvm
%global with_llvm_arg with_llvm=yes
%else
%global with_llvm_arg with_llvm=no
%endif

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:provsql only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.13.0
Release:	1PGSTY%{?dist}
Summary:	Semiring provenance and uncertainty management for PostgreSQL
License:	MIT
URL:		https://github.com/PierreSenellart/provsql
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if 0%{?rhel} == 8
# Keep upstream std::to_chars; EL8's base libstdc++ lacks its floating overloads.
BuildRequires:  gcc-toolset-15-gcc-c++ gcc-toolset-15-annobin-plugin-gcc
%else
BuildRequires:  gcc-c++
%endif
BuildRequires:  boost-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif
Requires:	postgresql%{pgmajorversion}-server
Requires:	postgresql%{pgmajorversion}-contrib

%description
ProvSQL adds semiring provenance and uncertainty management to PostgreSQL.
It rewrites queries to track tuple provenance and provides probability,
Shapley value, where-provenance, and temporal provenance evaluation.

ProvSQL must be loaded through shared_preload_libraries before running
CREATE EXTENSION provsql CASCADE.

%prep
%setup -q -n %{sname}-%{version}
%if 0%{?rhel} == 8
# Use the same C++17 headers for native objects and PGXS LLVM bitcode.
# Toolset compatibility archives provide newer libstdc++ features while
# retaining the system EL8 runtime libraries.
cat >> Makefile.internal <<'EOF'
override CC = /opt/rh/gcc-toolset-15/root/usr/bin/gcc
override CXX = /opt/rh/gcc-toolset-15/root/usr/bin/g++
%if 0%{?pgmajorversion} < 16
# PG14/15 walker callbacks need the pre-C23 semantics used by EL8 GCC 8.
override CFLAGS += -std=gnu17
%endif
override BITCODE_CXXFLAGS += --gcc-install-dir=/opt/rh/gcc-toolset-15/root/usr/lib/gcc/%{_target_cpu}-redhat-linux/15
EOF
%endif

%if 0%{?pgmajorversion} < 16 && %llvm
# PG14/15 headers retain register. Propagate the upstream native C++17
# requirements to the separate PGXS LLVM rule without replacing its flags.
cat >> Makefile.internal <<'EOF'
override BITCODE_CXXFLAGS += -std=c++17 -Wno-register
EOF
%endif

%build
PATH=%{pginstdir}/bin:$PATH %{__make} -f Makefile.internal PG_CXXFLAGS="-g" %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} -f Makefile.internal PG_CXXFLAGS="-g" %{?_smp_mflags} install DESTDIR=%{buildroot} %{with_llvm_arg}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%{pginstdir}/doc/extension/%{pname}.md
%if %llvm
%{pginstdir}/lib/bitcode/%{pname}/
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%endif

%changelog
* Fri Oct 23 2026 Ruohang Feng <rh@vonng.com> - 1.13.0-1PGSTY
- Use GCC Toolset 15 on EL8 to retain upstream shortest-roundtrip float text.
- Leave the EL9 and EL10 compiler paths and source code unchanged.

* Wed Oct 21 2026 Ruohang Feng <rh@vonng.com> - 1.13.0-1PGSTY
- Update to upstream 1.13.0.
- Enable PGXS LLVM output and preserve C++ DWARF debug information.
- Propagate C++17 flags to LLVM compilation with PostgreSQL 14 and 15.
- Include the EL8 compatibility patch in the source RPM.

* Sat Aug 08 2026 Vonng <rh@vonng.com> - 1.12.0-1PIGSTY
- Update to upstream PGXN 1.12.0
- Refresh the EL8 std::to_chars compatibility patch

* Fri Aug 07 2026 Vonng <rh@vonng.com> - 1.11.1-1PIGSTY
- Update to upstream PGXN 1.11.1
- Refresh the EL8 std::to_chars compatibility patch
- Restrict builds to active PostgreSQL 14 through 18 releases

* Sun Jul 19 2026 Vonng <rh@vonng.com> - 1.11.0-1PIGSTY
- Update to upstream PGXN 1.11.0
- Refresh the EL8 std::to_chars compatibility patch

* Fri Jun 19 2026 Vonng <rh@vonng.com> - 1.10.0-1PIGSTY
- https://pgxn.org/dist/provsql/1.10.0/
- Refresh the EL8 std::to_chars compatibility patch

* Thu Jun 11 2026 Vonng <rh@vonng.com> - 1.9.0-1PIGSTY
- https://pgxn.org/dist/provsql/1.9.0/
- Refresh the EL8 std::to_chars compatibility patch

* Thu Jun 04 2026 Vonng <rh@vonng.com> - 1.8.0-1PIGSTY
- https://pgxn.org/dist/provsql/1.8.0/

* Sun May 24 2026 Vonng <rh@vonng.com> - 1.7.1-1PIGSTY
- https://pgxn.org/dist/provsql/1.7.1/
* Thu May 14 2026 Vonng <rh@vonng.com> - 1.4.0-1PIGSTY
- https://pgxn.org/dist/provsql/1.4.0/
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 1.2.3-1PIGSTY
- https://github.com/PierreSenellart/provsql/releases/tag/v1.2.3
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 1.2.2-1PIGSTY
- Restrict builds to PostgreSQL 14+ to match extension metadata and tested support
- Initial RPM release
- https://github.com/PierreSenellart/provsql/releases/tag/v1.2.2
