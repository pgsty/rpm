%define haproxy_user    haproxy
%define haproxy_group   %{haproxy_user}
%define haproxy_homedir %{_localstatedir}/lib/haproxy
%define haproxy_confdir %{_sysconfdir}/haproxy
%define haproxy_datadir %{_datadir}/haproxy

%global _hardened_build 1
%global source0_sha256 7fa666d36d198275999e2a68dda44d3d37960f2f7aed3a595fb811f4fd0515b5
%global source1_sha256 89457600f60554d6fed74ca18491e99e5600899999615e834c59cd4dad8732de
%global source2_sha256 d9ecbd2b112e658f06ce6960a72fdc4303198c34d0a549850b91d0beb8300127
%global source3_sha256 234409fa4142e7f35fd1ee6bf54960f9d37382f34f517a95550fe3a90524eda9
%global source4_sha256 c2bb334d3b9320773a368e544c6f8c47e39b0f6e70be32aed38c39cf28adab11
%global source5_sha256 dc2fdd7eb120cfc4696d896340f397c84c8ef372c83b0d42ffbc547454c00688

Name:           haproxy
Version:        3.4.3
Release:        1PIGSTY%{?dist}
Summary:        HAProxy reverse proxy for high availability environments

License:        GPL-2.0-or-later AND LGPL-2.1-or-later
URL:            https://www.haproxy.org/
Source0:        https://www.haproxy.org/download/%(v=%{version}; echo ${v%.*})/src/%{name}-%{version}.tar.gz
Source1:        %{name}.cfg
Source2:        %{name}.logrotate
Source3:        %{name}.sysconfig
Source4:        halog.1
Source5:        %{name}-sysusers.conf

BuildRequires:  gcc
BuildRequires:  libxcrypt-devel
BuildRequires:  lua-devel
BuildRequires:  make
BuildRequires:  pcre2-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  systemd-rpm-macros
Requires:       openssl-libs >= 1.1.1k
BuildRequires:  openssl-devel

Requires(pre):  systemd
Recommends:     logrotate
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
echo "%{source0_sha256}  %{SOURCE0}" | sha256sum -c -
echo "%{source1_sha256}  %{SOURCE1}" | sha256sum -c -
echo "%{source2_sha256}  %{SOURCE2}" | sha256sum -c -
echo "%{source3_sha256}  %{SOURCE3}" | sha256sum -c -
echo "%{source4_sha256}  %{SOURCE4}" | sha256sum -c -
echo "%{source5_sha256}  %{SOURCE5}" | sha256sum -c -
%autosetup

%build
quic_compat=
if ! pkg-config --atleast-version=3.5.2 openssl; then
    quic_compat="USE_QUIC_OPENSSL_COMPAT=1"
fi

%{__make} %{?_smp_mflags} \
    TARGET="linux-glibc" \
    EXTRAVERSION="-%{release}" \
    USE_OPENSSL=1 \
    USE_QUIC=1 \
    USE_PCRE2=1 \
    USE_PCRE2_JIT=1 \
    USE_SLZ=1 \
    USE_LUA=1 \
    USE_PROMEX=1 \
    CC=%{__cc} \
    CFLAGS="%{build_cflags}" \
    LDFLAGS="%{build_ldflags}" \
    OPT_CFLAGS="" \
    ARCH_FLAGS="" \
    EXTRA="admin/halog/halog admin/iprange/iprange admin/iprange/ip6range" \
    ${quic_compat}

%{__make} -C admin/systemd PREFIX=%{_prefix} SBINDIR=%{_sbindir}

%install
%{__make} install-bin install-man \
    DESTDIR=%{buildroot} \
    PREFIX=%{_prefix} \
    SBINDIR=%{_sbindir}

%{__install} -p -D -m 0644 admin/systemd/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{haproxy_confdir}/%{name}.cfg
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -p -D -m 0644 %{SOURCE4} %{buildroot}%{_mandir}/man1/halog.1
# Keep the chroot root-owned and non-writable by the service account.
%{__install} -d -m 0755 %{buildroot}%{haproxy_homedir}
%{__install} -d -m 0755 %{buildroot}%{haproxy_datadir}
%{__install} -d -m 0755 %{buildroot}%{haproxy_confdir}/conf.d
%{__install} -d -m 0755 %{buildroot}%{_bindir}
%{__install} -p -m 0755 admin/halog/halog %{buildroot}%{_bindir}/halog
%{__install} -p -m 0755 admin/iprange/iprange %{buildroot}%{_bindir}/iprange
%{__install} -p -m 0755 admin/iprange/ip6range %{buildroot}%{_bindir}/ip6range

for httpfile in $(find ./examples/errorfiles/ -type f)
do
    %{__install} -p -m 0644 $httpfile %{buildroot}%{haproxy_datadir}
done

%{__rm} -rf ./examples/errorfiles/
find ./examples/* -type f ! -name "*.cfg" -exec %{__rm} -f "{}" \;

# Convert the only ISO-8859-1 document without rewriting unrelated text files.
iconv -f ISO-8859-1 -t UTF-8 \
    -o doc/internals/connection-scale.txt{.utf8,}
touch -c -r doc/internals/connection-scale.txt{,.utf8}
%{__mv} -f doc/internals/connection-scale.txt{.utf8,}

%{__install} -m 0644 -D %{SOURCE5} %{buildroot}%{_sysusersdir}/%{name}.conf

%{__mv} -f doc/{gpl,lgpl}.txt .
%{__rm} -f doc/%{name}.1 examples/%{name}.init

%pre
%sysusers_create_package %{name} %SOURCE5

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE gpl.txt lgpl.txt
%doc CHANGELOG README.md doc/* examples/
%dir %{haproxy_homedir}
%dir %{haproxy_confdir}
%dir %{haproxy_confdir}/conf.d
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
%{_sysusersdir}/%{name}.conf

%changelog
* Fri Jul 31 2026 Ruohang Feng <rh@vonng.com> 3.4.3-1PIGSTY
- Update to 3.4.3.
- Generate the vendor unit from upstream and load haproxy.cfg plus conf.d.
- Create the package-owned /etc/haproxy/conf.d directory.
- Modernize build flags and package metadata.
- Remove the obsolete libsystemd build dependency.
- Keep the chroot root-owned and align sysconfig with upstream EXTRAOPTS.
- Use native OpenSSL QUIC APIs when the build platform provides them.
- Ship a listener-free default config and resilient log rotation.
- Verify every source input against a fixed SHA-256 digest.

* Tue Jul 07 2026 Devrim Gündüz <devrim@gunduz.org> 3.4.2-1PGDG
- Update to 3.4.2 per changes described at:
  https://mail-archive.com/haproxy@formilux.org/msg47291.html
