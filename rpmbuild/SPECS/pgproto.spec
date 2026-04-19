%global pname pgproto
%global sname pgproto
%global pginstdir /usr/pgsql-%{pgmajorversion}

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.3.3
Release:	1PIGSTY%{?dist}
Summary:	Native Protobuf support for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/Apaezmx/pgproto
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pgproto/0.3.3/pgproto-0.3.3.zip

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pgproto adds native Protobuf parsing, mutation, indexing, and JSON conversion
support to PostgreSQL.

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
%setup -q -n %{sname}-%{version}
# Guard against AppleDouble metadata files accidentally mirrored from macOS.
find . -name '._*' -delete

%build
PATH=%{pginstdir}/bin:$PATH %{__make}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Sat Apr 18 2026 Vonng <rh@vonng.com> - 0.3.3-1PIGSTY
- Update to upstream 0.3.3 with the normalized PGXN source tarball
- Switch to the vendored protobuf tree used by the current Debian recipe
- Drop the obsolete utf8_range header patch because upstream now links the
  bundled utf8_range implementation directly
- Delete stray AppleDouble files in %prep so polluted mirrors do not get
  compiled as C sources

* Thu Apr 16 2026 Vonng <rh@vonng.com> - 0.2.18-1PIGSTY
- Update to upstream 0.2.18 with the normalized PGXN source tarball
- Keep forcing utf8_range to the bundled naive path because the PGXS build still only links naive.o
- Build pgproto serially to avoid the vendored upb jobserver/LTO failures seen on EL9

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.2.4-1PIGSTY
- Update to upstream 0.2.4 with the normalized pgproto-0.2.4.tar.gz source tarball
- Keep forcing vendored utf8_range to the bundled naive implementation on
  EL9A because upstream still only links naive.o during the PGXS build
- Build pgproto serially to avoid EL9 make jobserver/LTO failures seen with
  the vendored upb build

* Thu Apr 09 2026 Vonng <rh@vonng.com> - 0.2.1-2PIGSTY
- Force vendored utf8_range to use the bundled naive implementation because
  the mirrored source tarball does not include the SIMD utf8_range2 sources.
- Build pgproto serially to avoid EL9 make jobserver/LTO failures seen with
  parallel make in the vendored upb build.

* Sun Apr 05 2026 Vonng <rh@vonng.com> - 0.2.1-1PIGSTY
- Initial RPM release, packaged from the upstream 0.2.1 source tree with
  vendored upb/utf8_range submodules mirrored into the source tarball
