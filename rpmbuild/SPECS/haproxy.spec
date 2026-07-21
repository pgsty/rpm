%define haproxy_user    haproxy
%define haproxy_group   %{haproxy_user}
%define haproxy_homedir %{_localstatedir}/lib/haproxy
%define haproxy_confdir %{_sysconfdir}/haproxy
%define haproxy_datadir %{_datadir}/haproxy

%global _hardened_build 1

Name:           haproxy
Version:        3.4.2
Release:        1PGDG%{?dist}
Summary:        HAProxy reverse proxy for high availability environments

License:        GPLv2+
URL:            https://www.haproxy.org/
Source0:        https://www.haproxy.org/download/3.4/src/%{name}-%{version}.tar.gz
Source1:        %{name}.service
Source2:        %{name}.cfg
Source3:        %{name}.logrotate
Source4:        %{name}.sysconfig
Source5:        halog.1
Source6:        %{name}-sysusers.conf
Source7:        %{name}-tmpfiles.d

BuildRequires:  gcc lua-devel pcre2-devel make
BuildRequires:  systemd-devel systemd
%if 0%{?suse_version} >= 1500
Requires:       libopenssl3
BuildRequires:  libopenssl-3-devel
%endif
%if 0%{?fedora} >= 42 || 0%{?rhel} >= 8
Requires:       openssl-libs >= 1.1.1k
BuildRequires:  openssl-devel
%endif

%{?systemd_requires}

%description
HAProxy is a TCP/HTTP reverse proxy which is particularly suited for high
availability environments. Indeed, it can:
 - route HTTP requests depending on statically assigned cookies
 - spread load among several servers while assuring server persistence
   through the use of HTTP cookies
 - switch to backup servers in the event a main one fails
 - accept connections to special ports dedicated to service monitoring
 - stop accepting connections without breaking existing ones
 - add, modify, and delete HTTP headers in both directions
 - block requests matching particular patterns
 - report detailed status to authenticated users from a URI
   intercepted from the application

%prep
%setup -q

%build
regparm_opts=
%ifarch %ix86 x86_64
regparm_opts="USE_REGPARM=1"
%endif

%{__make} %{?_smp_mflags} CPU="generic" TARGET="linux-glibc" USE_OPENSSL=1 USE_PCRE2=1 USE_SLZ=1 USE_LUA=1 USE_CRYPT_H=1 USE_LINUX_TPROXY=1 USE_GETADDRINFO=1 USE_PROMEX=1 DEFINE=-DMAX_SESS_STKCTR=12 ${regparm_opts} \
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 8
    ADDLIB="%{build_ldflags}" \
%endif
    ADDINC="%{build_cflags}"

%{__make} admin/halog/halog \
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 8
    ADDLIB="%{build_ldflags}" \
%endif
    ADDINC="%{build_cflags}"

pushd admin/iprange
%{__make} \
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 8
    LDFLAGS="%{build_ldflags}" \
%endif
    OPTIMIZE="%{build_cflags}"
popd

%install
%{__make} install-bin DESTDIR=%{buildroot} PREFIX=%{_prefix} SBINDIR=%{_sbindir} TARGET="linux2628"
%{__make} install-man DESTDIR=%{buildroot} PREFIX=%{_prefix}

%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{haproxy_confdir}/%{name}.cfg
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -p -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -p -D -m 0644 %{SOURCE5} %{buildroot}%{_mandir}/man1/halog.1
%{__install} -d -m 0755 %{buildroot}%{haproxy_homedir}
%{__install} -d -m 0755 %{buildroot}%{haproxy_datadir}
%{__install} -d -m 0755 %{buildroot}%{_bindir}
%{__install} -p -m 0755 ./admin/halog/halog %{buildroot}%{_bindir}/halog
%{__install} -p -m 0755 ./admin/iprange/iprange %{buildroot}%{_bindir}/iprange
%{__install} -p -m 0755 ./admin/iprange/ip6range %{buildroot}%{_bindir}/ip6range

for httpfile in $(find ./examples/errorfiles/ -type f)
do
    %{__install} -p -m 0644 $httpfile %{buildroot}%{haproxy_datadir}
done

%{__rm} -rf ./examples/errorfiles/
find ./examples/* -type f ! -name "*.cfg" -exec %{__rm} -f "{}" \;

for textfile in $(find ./ -type f -name '*.txt')
do
    %{__mv} $textfile $textfile.old
    iconv --from-code ISO8859-1 --to-code UTF-8 --output $textfile $textfile.old
    %{__rm} -f $textfile.old
done

%{__install} -m 0644 -D %{SOURCE6} %{buildroot}%{_sysusersdir}/%{name}-pgdg.conf
%{__mkdir} -p %{buildroot}/%{_tmpfilesdir}
%{__install} -m 0644 %{SOURCE7} %{buildroot}/%{_tmpfilesdir}/%{name}.conf

%pre
%sysusers_create_package %{name} %SOURCE6

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%doc doc/* examples/*
%doc CHANGELOG VERSION
%license LICENSE
%dir %{haproxy_homedir}
%dir %{haproxy_confdir}
%dir %{haproxy_datadir}
%{haproxy_datadir}/*
%config(noreplace) %{haproxy_confdir}/%{name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/%{name}.service
%{_sbindir}/%{name}
%{_bindir}/halog
%{_bindir}/iprange
%{_bindir}/ip6range
%{_mandir}/man1/*
%{_sysusersdir}/%{name}-pgdg.conf
%{_tmpfilesdir}/%{name}.conf

%changelog
* Tue Jul 07 2026 Devrim Gündüz <devrim@gunduz.org> 3.4.2-1PGDG
- Update to 3.4.2 per changes described at:
  https://mail-archive.com/haproxy@formilux.org/msg47291.html
