%global pname vector
%global sname pgvector
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global llvm_binpath /usr/bin

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.8.6
Release:	1PGSTY%{?dist}
Summary:	Open-source vector similarity search for Postgres
License:	PostgreSQL
URL:		https://github.com/%{sname}/%{sname}/
Source0:	%{sname}-%{version}.tar.gz

# To be removed when upstream releases a version with this patch:
# https://github.com/pgvector/pgvector/pull/311

BuildRequires:	postgresql%{pgmajorversion}-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
Open-source vector similarity search for Postgres.

Store your vectors with the rest of your data. Supports:

* exact and approximate nearest neighbor search
* single-precision, half-precision, binary, and sparse vectors
* L2 distance, inner product, cosine distance, L1 distance, Hamming distance,
  and Jaccard distance
* any language with a Postgres client

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} OPTFLAGS="" LLVM_BINPATH=%{llvm_binpath}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot} OPTFLAGS="" LLVM_BINPATH=%{llvm_binpath}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%dir %{pginstdir}/include/server/extension/vector/
%{pginstdir}/include/server/extension/vector/*.h

%if %llvm
   %{pginstdir}/lib/bitcode/%{pname}*.bc
   %{pginstdir}/lib/bitcode/%{pname}/src/*.bc
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.8.6-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Thu Jul 30 2026 Vonng <rh@vonng.com> - 0.8.6-1PIGSTY
- Update to upstream PGXN 0.8.6
- Disable upstream -march=native for portable builder artifacts

* Sun Jul 19 2026 Vonng <rh@vonng.com> - 0.8.5-1PIGSTY
- Update to upstream PGXN 0.8.5

* Wed Jul 01 2026 Vonng <rh@vonng.com> - 0.8.4-1PIGSTY
- Update to upstream 0.8.4

* Fri Jun 19 2026 Vonng <rh@vonng.com> - 0.8.3-1PIGSTY
- https://pgxn.org/dist/vector/0.8.3/
- Use system llvm-lto path for builder LLVM version compatibility

* Thu Feb 26 2026 Ruohang Feng <rh@vonng.com> - 0.8.2-1PIGSTY
* Sun Sep 07 2025 Ruohang Feng <rh@vonng.com> - 0.8.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
