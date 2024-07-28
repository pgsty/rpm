%define debug_package %{nil}
%global pname pgmq
%global sname pgmq
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.2.1
Release:	1PIGSTY%{?dist}
Summary:	A lightweight message queue. Like AWS SQS and RSMQ but on Postgres.
License:	PostgreSQL
URL:		https://github.com/tembo-io/pgmq
#           https://github.com/tembo-io/pgmq/archive/refs/tags/v1.2.1.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
Postgres Message Queue (PGMQ) -- A lightweight message queue. Like AWS SQS and RSMQ but on Postgres.
Lightweight - No background worker or external dependencies, just Postgres functions packaged in an extension
Guaranteed "exactly once" delivery of messages to a consumer within a visibility timeout
API parity with AWS SQS and RSMQ
Messages stay in the queue until explicitly removed
Messages can be archived, instead of deleted, for long-term retention and replayability

%install
%{__rm} -rf %{buildroot}
install -d %{buildroot}%{pginstdir}/lib/
install -d %{buildroot}%{pginstdir}/share/extension/
install -m 755 %{_sourcedir}/%{pname}_%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so %{buildroot}%{pginstdir}/lib/
install -m 644 %{_sourcedir}/%{pname}_%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}-*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 %{_sourcedir}/%{pname}_%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Sat Jun 29 2024 Vonng <rh@vonng.com> - 1.2.1
* Sun May 5 2024 Vonng <rh@vonng.com> - 1.1.1
- Initial RPM release, used by Pigsty <https://pigsty.io>