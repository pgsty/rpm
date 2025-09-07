%global pname vector
%global sname pgvector

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	0.8.1
Release:	1PGDG%{?dist}
Summary:	Open-source vector similarity search for Postgres
License:	PostgreSQL
URL:		https://github.com/%{sname}/%{sname}/
Source0:	https://github.com/%{sname}/%{sname}/archive/refs/tags/v%{version}.tar.gz

# To be removed when upstream releases a version with this patch:
# https://github.com/pgvector/pgvector/pull/311
Patch0:		pgvector-0.6.2-fixillegalinstructionrror.patch

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
Open-source vector similarity search for Postgres.

Store your vectors with the rest of your data. Supports:

* exact and approximate nearest neighbor search
* single-precision, half-precision, binary, and sparse vectors
* L2 distance, inner product, cosine distance, L1 distance, Hamming distance,
  and Jaccard distance
* any language with a Postgres client

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgvector
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm => 19.0
%endif

%description llvmjit
This package provides JIT support for pgvector
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

#Remove header file, we don't need it right now:
%{__rm} %{buildroot}%{pginstdir}/include/server/extension/%{pname}/%{pname}.h

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension//%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%dir %{pginstdir}/include/server/extension/vector/
%{pginstdir}/include/server/extension/vector/*.h

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{pname}*.bc
   %{pginstdir}/lib/bitcode/%{pname}/src/*.bc
%endif

%changelog
* Sun Sep 07 2025 Ruohang Feng <rh@vonng.com> - 0.8.1-1PIGSTY
- Initial RPM release, used by Pigsty <https://pigsty.io>
