%define haproxy_user    haproxy
%define haproxy_group   %{haproxy_user}
%define haproxy_homedir %{_localstatedir}/lib/haproxy
%define haproxy_confdir %{_sysconfdir}/haproxy
%define haproxy_datadir %{_datadir}/haproxy

# HAProxy registers its init calls through custom ELF sections that are
# collected with linker defined start/stop symbols. Link time optimization is
# not supported upstream and is not effective here anyway, because HAProxy
# links with LDFLAGS only and would fall back to the fat objects.
%global _lto_cflags %{nil}

%global source0_sha256 7fa666d36d198275999e2a68dda44d3d37960f2f7aed3a595fb811f4fd0515b5
%global source1_sha256 6fb18a31be22e21d57c2f26a4bb9160cc2853f5e98e74cbf7e50a06ae57f79db
# The packaged vendor unit is a downstream file. Verify that the upstream
# template it was derived from has not changed, so an upstream revision fails
# the build instead of silently diverging from the shipped unit.
%global service_in_sha256 937ff126740ce81e487929cb3c927c608de18b86396e0939bb5fd632897db783

# Keep documentation of every subpackage under one directory.
%global _docdir_fmt %{name}

Name:           haproxy
Version:        3.4.3
Release:        2PIGSTY%{?dist}
Summary:        HAProxy reverse proxy for high availability environments

License:        GPL-2.0-or-later AND LGPL-2.1-or-later
URL:            https://www.haproxy.org/
Source0:        https://www.haproxy.org/download/%(v=%{version}; echo ${v%.*})/src/%{name}-%{version}.tar.gz
Source1:        %{name}-utils-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libxcrypt-devel
BuildRequires:  lua-devel
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  pcre2-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3-sphinx
BuildRequires:  systemd-rpm-macros

Requires(pre):  shadow-utils
Recommends:     logrotate
# The packaged haproxy-reload helper drives the master CLI socket through socat.
Recommends:     socat
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

%package doc
Summary:        Documentation for HAProxy
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc
Reference documentation, internal design notes, and configuration examples for
HAProxy. The material is not needed to run the service.

%prep
echo "%{source0_sha256}  %{SOURCE0}" | sha256sum -c -
echo "%{source1_sha256}  %{SOURCE1}" | sha256sum -c -
%autosetup -a 1
echo "%{service_in_sha256}  admin/systemd/%{name}.service.in" | sha256sum -c -

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

%{__make} -C doc/lua-api man

%install
# install-admin ships the upstream master CLI helpers haproxy-reload and
# haproxy-dump-certs. EXTRA is intentionally not passed here: halog, iprange,
# and ip6range are user commands and belong in %{_bindir}, not %{_sbindir}.
%{__make} install-bin install-admin install-man \
    DESTDIR=%{buildroot} \
    PREFIX=%{_prefix} \
    SBINDIR=%{_sbindir}

%{__install} -d -m 0755 %{buildroot}%{_bindir}
%{__install} -p -m 0755 admin/halog/halog %{buildroot}%{_bindir}/halog
%{__install} -p -m 0755 admin/iprange/iprange %{buildroot}%{_bindir}/iprange
%{__install} -p -m 0755 admin/iprange/ip6range %{buildroot}%{_bindir}/ip6range
%{__install} -p -D -m 0644 haproxy-utils/halog.1 %{buildroot}%{_mandir}/man1/halog.1
%{__install} -p -D -m 0644 doc/lua-api/_build/man/%{name}-lua.1 \
    %{buildroot}%{_mandir}/man1/%{name}-lua.1

# Downstream packaging assets, shared byte for byte with the DEB recipe.
%{__install} -p -D -m 0644 haproxy-utils/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
%{__install} -p -D -m 0644 haproxy-utils/%{name}.cfg %{buildroot}%{haproxy_confdir}/%{name}.cfg
%{__install} -p -D -m 0644 haproxy-utils/%{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -p -D -m 0644 haproxy-utils/%{name}.rsyslog %{buildroot}%{_sysconfdir}/rsyslog.d/49-%{name}.conf
%{__install} -p -D -m 0644 haproxy-utils/%{name}.tmpfiles %{buildroot}%{_tmpfilesdir}/%{name}.conf
%{__install} -p -D -m 0644 haproxy-utils/%{name}-sysusers.conf %{buildroot}%{_sysusersdir}/%{name}.conf
%{__install} -d -m 0755 %{buildroot}%{_sysconfdir}/default
%{__install} -p -D -m 0644 haproxy-utils/%{name}.default %{buildroot}%{_sysconfdir}/default/%{name}

# Keep the chroot root-owned and non-writable by the service account. The dev
# subdirectory is the mount point for the optional host /dev/log binding.
%{__install} -d -m 0755 %{buildroot}%{haproxy_homedir}
%{__install} -d -m 0755 %{buildroot}%{haproxy_homedir}/dev
%{__install} -d -m 0755 %{buildroot}%{haproxy_datadir}
%{__install} -d -m 0755 %{buildroot}%{haproxy_confdir}/conf.d

# The DEB recipe installs the very same set into the same directory.
for httpfile in ./examples/errorfiles/*.http
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

%{__mv} -f doc/{gpl,lgpl}.txt .
%{__rm} -f doc/%{name}.1 examples/%{name}.init
%{__rm} -rf doc/lua-api/_build doc/lua-api/.doctrees

%pre
getent group %{haproxy_group} >/dev/null || \
    groupadd -r %{haproxy_group} || exit 1
getent passwd %{haproxy_user} >/dev/null || \
    useradd -r -g %{haproxy_group} -d %{haproxy_homedir} -s /sbin/nologin \
        -c 'HAProxy User' %{haproxy_user} || exit 1
exit 0

%post
%{_bindir}/systemd-tmpfiles --create %{_tmpfilesdir}/%{name}.conf >/dev/null 2>&1 || :
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service
# HAProxy is a load balancer: reload the running instance instead of
# restarting it. ExecReload validates the configuration and then signals the
# master to re-execute, which picks up the freshly installed binary while
# established connections drain on the previous workers.
if [ $1 -ge 1 ] && [ -d /run/systemd/system ]; then
    %{_bindir}/systemctl try-reload-or-restart %{name}.service >/dev/null 2>&1 || :
fi

%files
%license LICENSE gpl.txt lgpl.txt
%doc README.md
%dir %{haproxy_homedir}
%dir %{haproxy_homedir}/dev
%dir %{_sysconfdir}/default
%dir %{haproxy_confdir}
%dir %{haproxy_confdir}/conf.d
%dir %{haproxy_datadir}
%{haproxy_datadir}/*
%config(noreplace) %{haproxy_confdir}/%{name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/rsyslog.d/49-%{name}.conf
%config(noreplace) %{_sysconfdir}/default/%{name}
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.conf
%{_sbindir}/%{name}
%{_sbindir}/%{name}-reload
%{_sbindir}/%{name}-dump-certs
%{_bindir}/halog
%{_bindir}/iprange
%{_bindir}/ip6range
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-lua.1*
%{_mandir}/man1/halog.1*

%files doc
%doc CHANGELOG doc/* examples/

%changelog
* Sun Aug 02 2026 Ruohang Feng <rh@vonng.com> 3.4.3-2PIGSTY
- Reload instead of restart on package upgrade.
- Ship the vendor unit as a shared downstream asset and verify the upstream
  template against a fixed SHA-256 digest.
- Set RestartSec so Restart=always survives the systemd start rate limit.
- Set an explicit maxconn and a runtime stats socket in the baseline config.
- Ship no default network listener. The baseline serves the local runtime API
  socket only; deployments define their listeners in conf.d.
- Create the service account from the pre scriptlet so installation no longer
  depends on systemd-sysusers.
- Split the reference documentation into the haproxy-doc subpackage.
- Install the upstream master CLI helpers haproxy-reload and haproxy-dump-certs.
- Install the Lua API manual page.
- Ship the optional rsyslog integration and the runtime directory definition.
- Make the host /dev/log socket available inside the default chroot.
- Disable link time optimization, which is unsupported upstream and was
  ineffective here.
- Drop the redundant manual openssl-libs dependency and the obsolete
  _hardened_build definition.

* Fri Jul 31 2026 Ruohang Feng <rh@vonng.com> 3.4.3-1PIGSTY
- Update to 3.4.3.
- Bundle downstream packaging assets in haproxy-utils.tar.gz.
- Generate the standard debuginfo and debugsource subpackages.
- Generate the vendor unit from upstream and load haproxy.cfg plus conf.d.
- Create the package-owned /etc/haproxy/conf.d directory.
- Modernize build flags and package metadata.
- Remove the obsolete libsystemd build dependency.
- Use /etc/default/haproxy as the shared RPM and DEB environment interface.
- Use native OpenSSL QUIC APIs when the build platform provides them.
- Ship a conservative TCP baseline with stdout logging and loopback-only
  health, statistics, and Prometheus endpoints on port 9101.
- Remove obsolete sysconfig, daemon, pidfile, legacy syslog, and Web sample
  assumptions.
- Restore the upstream stick-counter limit; configurations using track-sc3 or
  above must set tune.stick-counters explicitly in the global section.
- Verify every source input against a fixed SHA-256 digest.

* Tue Jul 07 2026 Devrim Gündüz <devrim@gunduz.org> 3.4.2-1PGDG
- Update to 3.4.2 per changes described at:
  https://mail-archive.com/haproxy@formilux.org/msg47291.html
