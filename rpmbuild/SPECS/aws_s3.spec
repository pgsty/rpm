%define debug_package %{nil}
%global pname aws_s3
%global sname aws_s3
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.1
Release:	1PIGSTY%{?dist}
Summary:	aws_s3 postgres extension to import/export data from/to s3
License:	Apache-2.0
URL:		https://github.com/chimpler/postgres-aws-s3
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
Starting on Postgres version 11.1, AWS RDS added support for S3 import using the extension aws_s3.
It allows to import data from S3 within Postgres using the function aws_s3.table_import_from_s3 and export the data to S3 using the function aws_s3.query_export_to_s3.
In order to support development either on RDS or locally, we implemented our own aws_s3 extension that is
similar to the one provided in RDS. It was implemented in Python using the boto3 library.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%changelog
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.0
- Initial RPM release, used by Pigsty <https://pigsty.io>