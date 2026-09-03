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

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.3.3
Release:	1PGSTY%{?dist}
Summary:	A Postgres extension in C to compute statistics on arrays of numbers
License:	MIT
URL:		https://github.com/pjungwir/aggs_for_arrays
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
This Postgres extension provides various functions for operating on arrays, for instance taking the histogram of an array of numbers.
These functions are useful because if you have a lot values you want to aggregate, queries that fetch each value from a separate row can have poor performance. Storing all the values in a single row as a Postgres array can drastically improve query performance. For instance, computing a 1000-bucket histogram on one million float values stored in separate rows took 12 seconds in a simple benchmark, compared to 27 milliseconds with the array_to_hist function.
Using arrays in this way is a bit like a poor-man's column-store database: it lets you keep all the values for one attribute in one place. (It's also a bit like how in R and Pandas you often see parallel arrays rather than arrays of objects.) To simplify a little, imagine pulling one million floats off disk in a single 8MB chunk instead of asking the drive for one million separate reads. I wouldn't use this pattern if your arrays get updated a lot, lest you take a hit on writes (At least test first!), but if they are pretty stable then using arrays can greatly speed up reads.
With such an approach you could still use SQL or PLPGSQL, but these functions outperform such code, because the Postgres C API lets you skip a lot of the work for interfacing at those higher levels. For instance, the same benchmark gave 398ms for a SQL solution and 12 seconds for a plpgsql solution. We show further benchmark results below.
Note that despite the name, these functions are not true aggregate functions (summarizing multiple rows). Rather they do aggregate-like calculations on a single input array. If you want actual aggregates that take multiple input arrays, then you might be looking for my other extension, aggs_for_vecs. If this extension takes a column-store approach to your data, that one takes a row-store approach.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.3.3-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Tue Oct 29 2024 Vonng <rh@vonng.com> - 1.3.3
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.3.2
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
