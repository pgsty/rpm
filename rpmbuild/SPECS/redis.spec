%undefine _debugsource_packages
%global source0_sha256 7bf7975331511fdb788e85dae63964b128fccee1df026a10db57444babc9c9c4
%global redis_modules_abi 1
%global redis_modules_dir %{_libdir}/redis/modules

%bcond_without tests

Name:           redis
Version:        7.2.15
Release:        1PIGSTY%{?dist}
Summary:        A persistent key-value database
License:        BSD-3-Clause AND BSD-2-Clause AND MIT AND BSL-1.0
URL:            https://redis.io/
Source0:        https://download.redis.io/releases/redis-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  systemd-rpm-macros
%if %{with tests}
BuildRequires:  openssl
BuildRequires:  procps-ng
BuildRequires:  tcl
%if 0%{?rhel} < 10
BuildRequires:  tcltls
%endif
%endif
Requires:       logrotate
Requires(pre):  shadow-utils
%{?systemd_requires}

Provides:       bundled(fpconv)
Provides:       bundled(hdr_histogram)
Provides:       bundled(hiredis) = 1.2.0
Provides:       bundled(jemalloc) = 5.3.0
Provides:       bundled(linenoise) = 1.0
Provides:       bundled(lua-libs) = 5.1.5
Provides:       bundled(lzf)
Provides:       redis(modules_abi)%{?_isa} = %{redis_modules_abi}

%description
Redis is an advanced in-memory key-value store supporting strings, hashes,
lists, sets, sorted sets, streams, transactions, Pub/Sub, Lua scripting,
replication, Sentinel, persistence, and clustering.

%package devel
Summary:        Development header for Redis module development
License:        BSD-3-Clause
BuildArch:      noarch

%description devel
Header file and RPM macros required for building loadable Redis modules.

%prep
echo "%{source0_sha256}  %{SOURCE0}" | sha256sum -c -
%setup -q -n redis-%{version}

cp deps/jemalloc/COPYING COPYING-jemalloc
cp deps/lua/COPYRIGHT COPYRIGHT-lua
cp deps/hiredis/COPYING COPYING-hiredis
cp deps/hdr_histogram/LICENSE.txt LICENSE-hdrhistogram
cp deps/hdr_histogram/COPYING.txt COPYING-hdrhistogram
cp deps/fpconv/LICENSE.txt LICENSE-fpconv

%ifarch %{ix86} %arm x86_64 s390x
sed -e 's/--with-lg-quantum/--with-lg-page=12 --with-lg-quantum/' -i deps/Makefile
%endif
%ifarch ppc64 ppc64le aarch64
sed -e 's/--with-lg-quantum/--with-lg-page=16 --with-lg-quantum/' -i deps/Makefile
%endif

sed -ri \
    -e 's|^daemonize no$|daemonize yes|' \
    -e 's|^# supervised auto$|supervised auto|' \
    -e 's|^# unixsocket /run/redis.sock$|unixsocket /run/redis/redis.sock|' \
    -e 's|^# unixsocketperm 700$|unixsocketperm 770|' \
    -e 's|^pidfile /var/run/redis_6379.pid$|pidfile /run/redis/redis.pid|' \
    -e 's|^logfile ""$|logfile /var/log/redis/redis.log|' \
    -e 's|^dir \./$|dir /var/lib/redis|' redis.conf
sed -ri \
    -e 's|^protected-mode no$|protected-mode yes|' \
    -e 's|^daemonize no$|daemonize yes|' \
    -e '/^daemonize yes$/a supervised auto' \
    -e 's|^pidfile /var/run/redis-sentinel.pid$|pidfile /run/redis/sentinel.pid|' \
    -e 's|^logfile ""$|logfile /var/log/redis/sentinel.log|' \
    -e 's|^dir /tmp$|dir /var/lib/redis|' sentinel.conf

api=$(sed -n -e 's/#define REDISMODULE_APIVER_[0-9][0-9]* //p' src/redismodule.h)
test "$api" = "%{redis_modules_abi}"

%global make_flags DEBUG="" V="echo" LDFLAGS="%{build_ldflags}" CFLAGS+="%{build_cflags} -fPIC" INSTALL="install -p" PREFIX=%{buildroot}%{_prefix} MALLOC=jemalloc BUILD_TLS=yes BUILD_WITH_SYSTEMD=yes

%build
%{__make} %{?_smp_mflags} %{make_flags} all

%install
%{__make} %{make_flags} install

install -d \
    %{buildroot}%{_sysconfdir}/redis \
    %{buildroot}%{_sysconfdir}/logrotate.d \
    %{buildroot}%{_unitdir} \
    %{buildroot}%{_sharedstatedir}/redis \
    %{buildroot}%{_localstatedir}/log/redis \
    %{buildroot}%{redis_modules_dir} \
    %{buildroot}%{_includedir} \
    %{buildroot}%{_rpmmacrodir}

install -pm640 redis.conf %{buildroot}%{_sysconfdir}/redis/redis.conf
install -pm640 sentinel.conf %{buildroot}%{_sysconfdir}/redis/sentinel.conf
install -pm644 src/redismodule.h %{buildroot}%{_includedir}/redismodule.h

cat > %{buildroot}%{_sysconfdir}/logrotate.d/redis <<'EOF'
/var/log/redis/*.log {
    weekly
    rotate 10
    copytruncate
    delaycompress
    compress
    notifempty
    missingok
}
EOF

cat > %{buildroot}%{_unitdir}/redis.service <<'EOF'
[Unit]
Description=Redis persistent key-value database
Documentation=https://redis.io/docs/latest/
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=notify
User=redis
Group=redis
WorkingDirectory=/var/lib/redis
ExecStart=/usr/bin/redis-server /etc/redis/redis.conf --daemonize no --supervised systemd
RuntimeDirectory=redis
RuntimeDirectoryMode=0755
UMask=007
PrivateTmp=true
NoNewPrivileges=true
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
EOF

cat > %{buildroot}%{_unitdir}/redis-sentinel.service <<'EOF'
[Unit]
Description=Redis Sentinel
Documentation=https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=notify
User=redis
Group=redis
WorkingDirectory=/var/lib/redis
ExecStart=/usr/bin/redis-sentinel /etc/redis/sentinel.conf --daemonize no --supervised systemd
RuntimeDirectory=redis
RuntimeDirectoryMode=0755
UMask=007
PrivateTmp=true
NoNewPrivileges=true
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
EOF

cat > %{buildroot}%{_rpmmacrodir}/macros.redis <<'EOF'
%%redis_version %{version}
%%redis_modules_abi %{redis_modules_abi}
%%redis_modules_dir %%{_libdir}/redis/modules
EOF

%check
%if %{with tests}
./utils/gen-test-certs.sh
./runtest --clients 1 --verbose --no-latency \
    --skiptest "diskless no replicas drop during rdb pipe" \
    --skiptest "diskless slow replicas drop during rdb pipe" \
    --skiptest "diskless fast replicas drop during rdb pipe" \
    --skiptest "diskless all replicas drop during rdb pipe"
%if 0%{?rhel} < 10
# TclTLS can deadlock on large bidirectional buffers in containers. Both
# skipped cases are exercised by the normal suite above.
./runtest --clients 1 --tls --verbose --no-latency \
    --skiptest "For unauthenticated clients output buffer is limited" \
    --skiptest "Test child sending info" \
    --skiptest "diskless no replicas drop during rdb pipe" \
    --skiptest "diskless slow replicas drop during rdb pipe" \
    --skiptest "diskless fast replicas drop during rdb pipe" \
    --skiptest "diskless all replicas drop during rdb pipe"
%else
# EPEL 10 does not provide TclTLS. Keep the normal upstream suite above and
# exercise both TLS server and client binaries with mutual authentication.
tls_pid="$PWD/redis-tls-smoke.pid"
tls_cleanup() {
    test ! -f "$tls_pid" || kill "$(cat "$tls_pid")" 2>/dev/null || :
}
trap tls_cleanup EXIT
./src/redis-server --port 0 --tls-port 16380 \
    --tls-cert-file tests/tls/redis.crt \
    --tls-key-file tests/tls/redis.key \
    --tls-ca-cert-file tests/tls/ca.crt \
    --daemonize yes --pidfile "$tls_pid" \
    --logfile "$PWD/redis-tls-smoke.log" --dir "$PWD"
tls_ready=0
for i in $(seq 1 50); do
    if ./src/redis-cli --tls --cacert tests/tls/ca.crt \
        --cert tests/tls/client.crt --key tests/tls/client.key \
        -p 16380 ping | grep -qx PONG; then
        tls_ready=1
        break
    fi
    sleep 0.1
done
test "$tls_ready" -eq 1
./src/redis-cli --tls --cacert tests/tls/ca.crt \
    --cert tests/tls/client.crt --key tests/tls/client.key \
    -p 16380 shutdown nosave
rm -f "$tls_pid"
trap - EXIT
%endif
./runtest-sentinel
%else
: tests disabled
%endif

%pre
getent group redis >/dev/null || groupadd -r redis
getent passwd redis >/dev/null || \
    useradd -r -g redis -d /var/lib/redis -s /sbin/nologin \
    -c 'Redis Database Server' redis
exit 0

%post
%systemd_post redis.service redis-sentinel.service

%preun
%systemd_preun redis.service redis-sentinel.service

%postun
%systemd_postun_with_restart redis.service redis-sentinel.service

%files
%license COPYING COPYRIGHT-lua COPYING-hiredis COPYING-jemalloc
%license LICENSE-hdrhistogram COPYING-hdrhistogram LICENSE-fpconv
%doc 00-RELEASENOTES MANIFESTO README.md
%config(noreplace) %{_sysconfdir}/logrotate.d/redis
%attr(0750, redis, root) %dir %{_sysconfdir}/redis
%attr(0640, redis, root) %config(noreplace) %{_sysconfdir}/redis/redis.conf
%attr(0640, redis, root) %config(noreplace) %{_sysconfdir}/redis/sentinel.conf
%dir %{_libdir}/redis
%dir %{redis_modules_dir}
%dir %attr(0750, redis, redis) %{_sharedstatedir}/redis
%dir %attr(0750, redis, redis) %{_localstatedir}/log/redis
%{_bindir}/redis-*
%{_unitdir}/redis.service
%{_unitdir}/redis-sentinel.service
%dir %attr(0755, redis, redis) %ghost %{_localstatedir}/run/redis

%files devel
%license COPYING
%{_includedir}/redismodule.h
%{_rpmmacrodir}/macros.redis

%changelog
* Sat Aug 01 2026 Ruohang Feng <rh@vonng.com> - 7.2.15-1PIGSTY
- Build Redis 7.2.15 as non-modular RPMs for EL8, EL9, and EL10.
- Provide redis, redis-devel, and redis-debuginfo with TLS and systemd support.
