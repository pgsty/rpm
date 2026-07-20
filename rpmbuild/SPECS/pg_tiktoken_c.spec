%global pname pg_tiktoken_c
%global sname pg_tiktoken_c
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global snapshot_commit fa2957b6ece483322f4c4ce0c374b3b77e22b892

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_tiktoken_c supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.1
Release:	1PIGSTY%{?dist}
Summary:	Fast tiktoken BPE tokenizer for PostgreSQL, implemented in C
License:	Apache-2.0
URL:		https://github.com/relytcloud/pg_tiktoken_c
Source0:	%{sname}-%{version}.tar.gz
#           upstream main snapshot fa2957b6ece483322f4c4ce0c374b3b77e22b892; no release tag is available
Patch0:		pg-tiktoken-c-1.1-destdir.patch
Patch1:		pg-tiktoken-c-1.1-correctness.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc pcre2-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_tiktoken_c brings OpenAI-compatible tiktoken BPE token counting,
encoding, and token-bounded text chunking into PostgreSQL. It is implemented
in C and bundles vocabularies for cl100k_base, o200k_base, r50k_base,
p50k_base, and p50k_edit.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%autosetup -p1 -n relytcloud-%{sname}-fa2957b

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} USE_PGXS=1 PG_CONFIG=%{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} USE_PGXS=1 PG_CONFIG=%{pginstdir}/bin/pg_config DESTDIR=%{buildroot} install

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%{pginstdir}/share/extension/%{pname}/

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Mon Jul 20 2026 Vonng <rh@vonng.com> - 1.1-1PIGSTY
- Initial RPM release from upstream snapshot fa2957b
- Bundle all five tiktoken vocabularies and honor DESTDIR during packaging
- Align o200k tokenization and model-family aliases with tiktoken behavior
- Reject oversized BPE pieces and impossible chunk limits instead of corrupting a backend or returning oversized chunks
- Build for PostgreSQL 14 through 18
