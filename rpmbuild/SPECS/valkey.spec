%undefine _debugsource_packages
%global source0_sha256 7d7232acd1b8a49b4e05d07a00b3ca8c801ae06ab633ca6a3423bc5f385ab7ee
%global valkey_modules_abi 1
%global valkey_modules_dir %{_libdir}/valkey/modules

%bcond_without tests

Name:           valkey
Version:        9.1.1
Release:        1PIGSTY%{?dist}
Summary:        A persistent key-value database
License:        BSD-3-Clause AND BSD-2-Clause AND MIT AND BSL-1.0 AND Apache-2.0
URL:            https://valkey.io/
Source0:        https://github.com/valkey-io/valkey/archive/refs/tags/%{version}.tar.gz#/valkey-%{version}.tar.gz
Patch0:         valkey-9.1.1-el8a-geosearch-zero-radius.patch

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
Provides:       bundled(ffc) = 26.03.02
Provides:       bundled(hdr_histogram)
Provides:       bundled(jemalloc) = 5.3.0
Provides:       bundled(libvalkey) = 0.4.0
Provides:       bundled(linenoise) = 1.0
Provides:       bundled(lua-libs) = 5.1.5
Provides:       bundled(lzf)
Provides:       valkey(modules_abi)%{?_isa} = %{valkey_modules_abi}

ExcludeArch:    %{ix86}

%description
Valkey is an open source, high-performance data structure server supporting
strings, hashes, lists, sets, sorted sets, streams, transactions, Pub/Sub,
Lua scripting, replication, Sentinel, persistence, and clustering.

%package devel
Summary:        Development header for Valkey module development
License:        BSD-3-Clause
BuildArch:      noarch

%description devel
Header file and RPM macros required for building loadable Valkey modules.

%prep
echo "%{source0_sha256}  %{SOURCE0}" | sha256sum -c -
%setup -q -n valkey-%{version}
%if 0%{?rhel} == 8
%ifarch aarch64
%patch -P 0 -p1
%endif
%endif

cp deps/jemalloc/COPYING COPYING-jemalloc
cp deps/lua/COPYRIGHT COPYRIGHT-lua
cp deps/libvalkey/COPYING COPYING-libvalkey
cp deps/hdr_histogram/LICENSE.txt LICENSE-hdrhistogram
cp deps/hdr_histogram/COPYING.txt COPYING-hdrhistogram
cp deps/fpconv/LICENSE.txt LICENSE-fpconv
sed -n '1,94p' deps/fast_float/ffc.h > LICENSE-fast-float
cp deps/gtest-parallel/LICENSE LICENSE-gtest-parallel

%ifarch %{ix86} %arm x86_64 s390x
sed -e 's/--with-lg-quantum/--with-lg-page=12 --with-lg-quantum/' -i deps/Makefile
%endif
%ifarch ppc64 ppc64le aarch64
sed -e 's/--with-lg-quantum/--with-lg-page=16 --with-lg-quantum/' -i deps/Makefile
%endif

sed -ri \
    -e 's|^daemonize no$|daemonize yes|' \
    -e 's|^# supervised auto$|supervised auto|' \
    -e 's|^# unixsocket /run/valkey.sock$|unixsocket /run/valkey/valkey.sock|' \
    -e 's|^# unixsocketperm 700$|unixsocketperm 770|' \
    -e 's|^pidfile /var/run/valkey_6379.pid$|pidfile /run/valkey/valkey.pid|' \
    -e 's|^logfile ""$|logfile /var/log/valkey/valkey.log|' \
    -e 's|^dir \./$|dir /var/lib/valkey|' valkey.conf
sed -ri \
    -e 's|^protected-mode no$|protected-mode yes|' \
    -e 's|^daemonize no$|daemonize yes|' \
    -e '/^daemonize yes$/a supervised auto' \
    -e 's|^pidfile /var/run/valkey-sentinel.pid$|pidfile /run/valkey/sentinel.pid|' \
    -e 's|^logfile ""$|logfile /var/log/valkey/sentinel.log|' \
    -e 's|^dir /tmp$|dir /var/lib/valkey|' sentinel.conf

api=$(sed -n -e 's/#define VALKEYMODULE_APIVER_[0-9][0-9]* //p' src/valkeymodule.h)
test "$api" = "%{valkey_modules_abi}"

%global make_flags DEBUG="" V="echo" LDFLAGS="%{build_ldflags}" CFLAGS+="%{build_cflags} -fPIC" PREFIX=%{buildroot}%{_prefix} MALLOC=jemalloc BUILD_WITH_SYSTEMD=yes BUILD_TLS=yes

%build
%{__make} %{?_smp_mflags} %{make_flags}

%install
%{__make} %{make_flags} install
rm -rf %{buildroot}%{_datadir}/valkey
# Keep Valkey co-installable with Redis. Upstream installs these compatibility
# symlinks by default, but they would conflict with the native Redis package.
rm -f %{buildroot}%{_bindir}/redis-*

install -d \
    %{buildroot}%{_sysconfdir}/valkey \
    %{buildroot}%{_sysconfdir}/logrotate.d \
    %{buildroot}%{_unitdir} \
    %{buildroot}%{_sharedstatedir}/valkey \
    %{buildroot}%{_localstatedir}/log/valkey \
    %{buildroot}%{valkey_modules_dir} \
    %{buildroot}%{_includedir} \
    %{buildroot}%{_rpmmacrodir}

install -pm640 valkey.conf %{buildroot}%{_sysconfdir}/valkey/valkey.conf
install -pm640 sentinel.conf %{buildroot}%{_sysconfdir}/valkey/sentinel.conf
install -pm644 src/valkeymodule.h %{buildroot}%{_includedir}/valkeymodule.h

cat > %{buildroot}%{_sysconfdir}/logrotate.d/valkey <<'EOF'
/var/log/valkey/*.log {
    weekly
    rotate 10
    copytruncate
    delaycompress
    compress
    notifempty
    missingok
}
EOF

cat > %{buildroot}%{_unitdir}/valkey.service <<'EOF'
[Unit]
Description=Valkey persistent key-value database
Documentation=https://valkey.io/topics/
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=notify
User=valkey
Group=valkey
WorkingDirectory=/var/lib/valkey
ExecStart=/usr/bin/valkey-server /etc/valkey/valkey.conf --daemonize no --supervised systemd
RuntimeDirectory=valkey
RuntimeDirectoryMode=0755
UMask=007
PrivateTmp=true
NoNewPrivileges=true
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
EOF

cat > %{buildroot}%{_unitdir}/valkey-sentinel.service <<'EOF'
[Unit]
Description=Valkey Sentinel
Documentation=https://valkey.io/topics/sentinel/
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=notify
User=valkey
Group=valkey
WorkingDirectory=/var/lib/valkey
ExecStart=/usr/bin/valkey-sentinel /etc/valkey/sentinel.conf --daemonize no --supervised systemd
RuntimeDirectory=valkey
RuntimeDirectoryMode=0755
UMask=007
PrivateTmp=true
NoNewPrivileges=true
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
EOF

cat > %{buildroot}%{_rpmmacrodir}/macros.valkey <<'EOF'
%%valkey_version %{version}
%%valkey_modules_abi %{valkey_modules_abi}
%%valkey_modules_dir %%{_libdir}/valkey/modules
EOF

%check
%if %{with tests}
./utils/gen-test-certs.sh
# Docker kernels can expose the MPTCP client API while rejecting MPTCP server
# sockets. The dual-channel replication unit also requires more than 2 GB of
# transient memory, so keep both environment-specific units out of RPM builds.
./runtest --clients 1 --verbose --dump-logs --no-latency \
    --tags -mptcp \
    --skipunit integration/dual-channel-replication
%if 0%{?rhel} < 10
# TclTLS can deadlock on large bidirectional buffers in containers. Both
# skipped cases are exercised by the normal suite above.
./runtest --clients 1 --tls --verbose --dump-logs --no-latency \
    --tags -mptcp \
    --skiptest "For unauthenticated clients output buffer is limited" \
    --skiptest "Test child sending info" \
    --skipunit integration/dual-channel-replication
%else
# EPEL 10 does not provide TclTLS. Keep the normal upstream suite above and
# exercise both TLS server and client binaries with mutual authentication.
tls_pid="$PWD/valkey-tls-smoke.pid"
tls_cleanup() {
    test ! -f "$tls_pid" || kill "$(cat "$tls_pid")" 2>/dev/null || :
}
trap tls_cleanup EXIT
./src/valkey-server --port 0 --tls-port 16381 \
    --tls-cert-file tests/tls/valkey.crt \
    --tls-key-file tests/tls/valkey.key \
    --tls-ca-cert-file tests/tls/ca.crt \
    --daemonize yes --pidfile "$tls_pid" \
    --logfile "$PWD/valkey-tls-smoke.log" --dir "$PWD"
tls_ready=0
for i in $(seq 1 50); do
    if ./src/valkey-cli --tls --cacert tests/tls/ca.crt \
        --cert tests/tls/client.crt --key tests/tls/client.key \
        -p 16381 ping | grep -qx PONG; then
        tls_ready=1
        break
    fi
    sleep 0.1
done
test "$tls_ready" -eq 1
./src/valkey-cli --tls --cacert tests/tls/ca.crt \
    --cert tests/tls/client.crt --key tests/tls/client.key \
    -p 16381 shutdown nosave
rm -f "$tls_pid"
trap - EXIT
%endif
./runtest-sentinel
%else
: tests disabled
%endif

%pre
getent group valkey >/dev/null || groupadd -r valkey
getent passwd valkey >/dev/null || \
    useradd -r -g valkey -d /var/lib/valkey -s /sbin/nologin \
    -c 'Valkey Database Server' valkey
exit 0

%post
%systemd_post valkey.service valkey-sentinel.service

%preun
%systemd_preun valkey.service valkey-sentinel.service

%postun
%systemd_postun_with_restart valkey.service valkey-sentinel.service

%files
%license COPYING COPYRIGHT-lua COPYING-libvalkey COPYING-jemalloc
%license LICENSE-hdrhistogram COPYING-hdrhistogram LICENSE-fpconv
%license LICENSE-fast-float LICENSE-gtest-parallel
%doc 00-RELEASENOTES README.md
%config(noreplace) %{_sysconfdir}/logrotate.d/valkey
%attr(0750, valkey, root) %dir %{_sysconfdir}/valkey
%attr(0640, valkey, root) %config(noreplace) %{_sysconfdir}/valkey/valkey.conf
%attr(0640, valkey, root) %config(noreplace) %{_sysconfdir}/valkey/sentinel.conf
%dir %{_libdir}/valkey
%dir %{valkey_modules_dir}
%dir %attr(0750, valkey, valkey) %{_sharedstatedir}/valkey
%dir %attr(0750, valkey, valkey) %{_localstatedir}/log/valkey
%{_bindir}/valkey-*
%{_unitdir}/valkey.service
%{_unitdir}/valkey-sentinel.service
%dir %attr(0755, valkey, valkey) %ghost %{_localstatedir}/run/valkey

%files devel
%license COPYING
%{_includedir}/valkeymodule.h
%{_rpmmacrodir}/macros.valkey

%changelog
* Sat Aug 01 2026 Ruohang Feng <rh@vonng.com> - 9.1.1-1PIGSTY
- Build Valkey 9.1.1 for EL8, EL9, and EL10.
- Provide valkey, valkey-devel, and valkey-debuginfo with TLS and systemd support.
