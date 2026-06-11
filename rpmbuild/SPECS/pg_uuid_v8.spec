%global pname pg_uuid_v8
%global sname pg_uuid_v8
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_uuid_v8 only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	1PIGSTY%{?dist}
Summary:	UUID v8 generator with embedded timestamps for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/ineron/pg_uuid_v8
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pg_uuid_v8/1.0.0/pg_uuid_v8-1.0.0.zip
#           Supported: PostgreSQL 14, 15, 16, 17, 18

BuildRequires:	gcc openssl-devel pkgconf-pkg-config
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Requires:	openssl

%description
pg_uuid_v8 provides UUID version 8 generation functions with steganographic
embedded timestamps for PostgreSQL.

%prep
%setup -q -n %{sname}-%{version}
# PostgreSQL 17+ resolves the unqualified uuid operator commutators in the
# upstream SQL against pg_catalog before the extension's public operators exist.
# Keep the extension non-relocatable and schema-pinned so the packaged SQL can
# reference the newly-created public operators deterministically.
patch -p1 --forward -f < %{_specdir}/patches/%{sname}-%{version}.patch
sed -i "s/^relocatable = true/relocatable = false\\nschema = 'public'/" %{pname}.control

%build
# Upstream PGXS would emit bitcode without a matching llvmjit subpackage here;
# disable LLVM for this initial package until a JIT payload is intentionally
# packaged and tested.
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} with_llvm=no

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} with_llvm=no

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id/*

%changelog
* Thu Jun 04 2026 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Initial RPM release for upstream PGXN 1.0.0
- Pin extension installation to public so uuid operator commutators resolve to
  the packaged operators on PostgreSQL 17 and 18
