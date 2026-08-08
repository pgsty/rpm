%global pname plruby
%global sname plruby
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:plruby 2.5.0 supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        2.5.0
Release:        2PIGSTY%{?dist}
Summary:        Ruby procedural language for PostgreSQL
License:        MIT
URL:            https://github.com/commandprompt/plruby
Source0:        %{sname}-%{version}.tar.gz
#               https://github.com/commandprompt/plruby/archive/refs/tags/v2.5.0.tar.gz
Patch0:         plruby-2.5.0-ruby-method-signatures.patch

BuildRequires:  gcc make
# Keep native AppStream filtering enabled; module_hotfixes=1 can mix Ruby ABIs.
%if 0%{?rhel} == 8
# Enable the supported ruby:3.3 module stream before resolving build deps.
BuildRequires:  (ruby-devel >= 3.3 with ruby-devel < 3.4)
%else
%if 0%{?rhel} == 9
# Use EL9's non-modular, full-life Ruby instead of a newer module stream.
BuildRequires:  (ruby-devel >= 3.0 with ruby-devel < 3.1)
%else
# EL10 ships non-modular Ruby 3.3.
BuildRequires:  (ruby-devel >= 3.3 with ruby-devel < 3.4)
%endif
%endif
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server
Requires:       postgresql%{pgmajorversion}-contrib

%description
PL/Ruby embeds the MRI Ruby interpreter as an untrusted PostgreSQL procedural
language. The package also includes the jsonb, hstore, and ltree transform
extensions shipped by upstream.

%if %llvm
%package llvmjit
Summary:        Just-in-time compilation support for %{sname}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:  llvm-devel >= 19.0 clang-devel >= 19.0
Requires:       llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for PL/Ruby and its transform extensions.
%endif

%prep
%autosetup -p1 -n %{sname}-%{version}

%build
for component in . jsonb_plruby hstore_plruby ltree_plruby; do
    PATH=%{pginstdir}/bin:$PATH %{__make} -C "$component" clean \
        PG_CONFIG=%{pginstdir}/bin/pg_config RUBY=%{_bindir}/ruby
    PATH=%{pginstdir}/bin:$PATH %{__make} -C "$component" %{?_smp_mflags} \
        PG_CONFIG=%{pginstdir}/bin/pg_config RUBY=%{_bindir}/ruby
done

%install
%{__rm} -rf %{buildroot}
for component in . jsonb_plruby hstore_plruby ltree_plruby; do
    PATH=%{pginstdir}/bin:$PATH %{__make} -C "$component" %{?_smp_mflags} \
        PG_CONFIG=%{pginstdir}/bin/pg_config RUBY=%{_bindir}/ruby \
        install DESTDIR=%{buildroot}
done

%files
%license LICENSE
%doc README.md CHANGELOG.md INSTALL
%{pginstdir}/lib/*plruby*.so
%{pginstdir}/share/extension/*plruby*.control
%{pginstdir}/share/extension/*plruby*--*.sql

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/*plruby*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Sat Aug 08 2026 Vonng <rh@vonng.com> - 2.5.0-2PIGSTY
- Pin the native Ruby 3 ABI selected on EL8, EL9, and EL10
- Rely on the generated libruby SONAME dependency at runtime

* Fri Aug 07 2026 Vonng <rh@vonng.com> - 2.5.0-1PIGSTY
- Initial RPM release for PL/Ruby 2.5.0 and PostgreSQL 14 through 18
- Package the jsonb, hstore, and ltree transform extensions
- Use typed Ruby method callbacks for GCC 15 compatibility
