%global sname	login_hook
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}


%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.8
Release:	1PGSTY%{?dist}
Summary:	Postgres database extension to execute some code on user login, comparable to Oracle's after logon trigger.
License:	GPL-3.0-only
URL:		https://github.com/splendiddata/%{sname}
Source0:	%{sname}-%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
Postgres database extension to execute some code on user login,
comparable to Oracle's after logon trigger.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
# No need to ship these files:
%{__rm} %{buildroot}%{pginstdir}/doc/extension/%{sname}.css
%{__rm} %{buildroot}%{pginstdir}/doc/extension/%{sname}.html

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.8-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Bump to Version_1.8

* Sat Nov 01 2025 Vonng <rh@vonng.com> - 1.7.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
