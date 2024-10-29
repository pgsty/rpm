%global pname aggs_for_arrays
%global sname aggs_for_arrays
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
Version:	1.3.3
Release:	1PIGSTY%{?dist}
Summary:	A Postgres extension in C to compute statistics on arrays of numbers
License:	MIT
URL:		https://github.com/pjungwir/aggs_for_arrays
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
This Postgres extension provides various functions for operating on arrays, for instance taking the histogram of an array of numbers.
These functions are useful because if you have a lot values you want to aggregate, queries that fetch each value from a separate row can have poor performance. Storing all the values in a single row as a Postgres array can drastically improve query performance. For instance, computing a 1000-bucket histogram on one million float values stored in separate rows took 12 seconds in a simple benchmark, compared to 27 milliseconds with the array_to_hist function.
Using arrays in this way is a bit like a poor-man's column-store database: it lets you keep all the values for one attribute in one place. (It's also a bit like how in R and Pandas you often see parallel arrays rather than arrays of objects.) To simplify a little, imagine pulling one million floats off disk in a single 8MB chunk instead of asking the drive for one million separate reads. I wouldn't use this pattern if your arrays get updated a lot, lest you take a hit on writes (At least test first!), but if they are pretty stable then using arrays can greatly speed up reads.
With such an approach you could still use SQL or PLPGSQL, but these functions outperform such code, because the Postgres C API lets you skip a lot of the work for interfacing at those higher levels. For instance, the same benchmark gave 398ms for a SQL solution and 12 seconds for a plpgsql solution. We show further benchmark results below.
Note that despite the name, these functions are not true aggregate functions (summarizing multiple rows). Rather they do aggregate-like calculations on a single input array. If you want actual aggregates that take multiple input arrays, then you might be looking for my other extension, aggs_for_vecs. If this extension takes a column-store approach to your data, that one takes a row-store approach.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%changelog
* Tue Oct 29 2024 Vonng <rh@vonng.com> - 1.3.3
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.3.2
- Initial RPM release, used by Pigsty <https://pigsty.io>