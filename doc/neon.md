# Neon 构建、RPM 打包与 Pigsty 集成研究

本文记录 Neon OSS 全栈的源码构建、功能验证、RPM 打包方案，以及后续接入 Pigsty 时需要补齐的生产控制面。这里交付的是研究与可复用构建资产，不直接修改 Pigsty 主仓库。

## 1. 版本选择与范围

截至 2026-08-24，Neon monorepo 没有统一的 SemVer release。上游公开 release 至少分为 storage、compute、proxy 三条流，不能把三条 release 的二进制随意拼装成一个部署：

- 当前 OSS `main` 最后提交：`8f60b04da47ffefe0e52bda2440134b42874eb75`，2026-05-25。
- 最新公开 storage release：`release-9129`，commit `5340423416b46c85841904f42c93be9af145c643`，2025-07-25。
- 最新公开 compute release：`release-compute-9073`，commit `98882548d80fdc2e5e28f2ea3c693307587b057e`。
- 最新公开 proxy release：`release-proxy-8853`，commit `58abce0207943f44ac801aebc4f3d881e90a6894`。

本轮为了研究当前公开源码并验证整个本地链路，固定当时 `main` 的单一 commit `8f60b04`，包版本为 `20260525`。这是一份明确标识的 snapshot，不宣称等价于 Neon 云服务的生产 release。若进入 Pigsty 生产集成，建议另建 release 分支，以 `release-9129` 为 storage 的可复现基线，逐项验证 compute/proxy 兼容性，而不是覆盖本轮 snapshot；这是 Pigsty 侧的版本策略，不代表 Neon 上游提供了统一 self-hosting LTS 或生产支持承诺。

Neon 当前只构建 patched PostgreSQL 14、15、16、17；上游尚无 PG18，不能用 Pigsty 的普通 PG18 或 vanilla PostgreSQL 替代。

固定的 PostgreSQL 子模块：

| PG | PostgreSQL | submodule commit |
|---|---:|---|
| 14 | 14.18 | `2155cb165d05f617eb2c8ad7e43367189b627703` |
| 15 | 15.13 | `2aaab3bb4a13557aae05bb2ae0ef0a132d0c4f85` |
| 16 | 16.9 | `a42351fcd41ea01edede1daed65f651e838988fc` |
| 17 | 17.5 | `1e01fcea2a6b38180021aa83e0051d95286d9096` |

## 2. 架构与数据链路

```text
client -> proxy -> patched PostgreSQL compute
                        |
                        | WAL proposer
                        v
              Safekeeper Paxos quorum
                        |
                        | pageserver pulls WAL
                        v
              Pageserver immutable layers <-> object storage
                        ^
                        | GetPage@LSN
                        |
                     compute

storage broker:      storage-node state pub/sub
storage controller:  pageserver / tenant shard / generation placement
endpoint storage:    LFC prewarm data 的上传/下载 remote-storage 前端
```

主要组件：

- `pageserver`：接收并处理 WAL，生成 immutable delta/image layer，按 LSN 向 compute 提供页面，并与对象存储交互。
- `safekeeper`：WAL durable layer；生产部署需要多数派，单节点只适合开发验证。
- `storage_broker`：无状态 gRPC pub/sub，传播 Safekeeper timeline 状态。
- `storage_controller`：管理 pageserver、tenant shard、attachment 与 generation；其数据库在生产环境必须可靠持久化。
- `compute_ctl` + patched PostgreSQL：启动无状态 compute；Neon 对 PostgreSQL core、WAL 格式、smgr 和 walproposer 有修改。
- `proxy` / `pg_sni_router`：连接路由入口。OSS 默认构建不含需要私有 `SUBZERO_ACCESS_TOKEN` 的 `rest_broker` 能力。
- `neon_local`：开发/测试控制面，可拉起 broker、controller、本地 controller PG、pageserver、safekeeper 和 endpoint storage；它不是生产控制面。

## 3. 源码与离线输入

GitHub 自动生成的 source archive 不包含四个 PostgreSQL submodule，不能直接作为完整 SRPM Source。源码包必须来自 recursive checkout，并固定主仓库和子模块 SHA。

本轮 RPM 输入：

| 文件 | 用途 | SHA-256 |
|---|---|---|
| `neon-20260525.tar.gz` | 主源码和 PG14-17 子模块 | `eef3e6a34d7fa41216d62755bd9f1e8bb631d9fd20d6cca37367ef7c2ff84215` |
| `neon-cargo-vendor-20260525.tar.gz` | `Cargo.lock` 对应的 742 个 crates.io/git dependency 目录 | `254dbb4c925c1ec3b647cb05537a9b84f1fb1afcde588b9add2ddc0d2c4aa0a6` |
| `protoc-25.1-linux-x86_64.zip` | EL9 自带 protoc 过旧时使用 | `ed8fca87a11c888fed329d6a59c34c7d436165f662a2c875246ddb1ac2b6dd50` |

源码归档排除 `.git`、build/target、AppleDouble 和 macOS xattrs，并用 commit 时间、owner 0/group 0 归一化。`vendor/revisions.json` 保留四个 PostgreSQL commit，使没有 `.git` 的 SRPM 仍能把正确 SHA 写入 PostgreSQL 版本。

Cargo vendor 是正式 `Source2`。SPEC 从第一条 Cargo 命令开始使用 `--locked --offline`；`Cargo.lock` 构建前后哈希必须一致。这样 SRPM rebuild 不依赖 crates.io、GitHub 或代理。

## 4. Ubuntu 24.04 源码构建

官方依赖：

```bash
apt-get update
apt-get install -y \
  build-essential libtool libreadline-dev zlib1g-dev flex bison \
  libseccomp-dev libssl-dev clang pkg-config libpq-dev cmake \
  postgresql-client protobuf-compiler libprotobuf-dev \
  libcurl4-openssl-dev openssl python3-poetry lsof libicu-dev \
  git ca-certificates
```

最低要求：Rust 1.88.0、`protoc >= 3.15`、Python 3.11+。本轮实际使用 `rustc 1.88.0`、`cargo 1.88.0`、`libprotoc 3.21.12`。

完整 release + testing build：

```bash
git clone --recursive https://github.com/neondatabase/neon.git
cd neon
git checkout 8f60b04da47ffefe0e52bda2440134b42874eb75
git submodule update --init --recursive

export GIT_VERSION=8f60b04da47ffefe0e52bda2440134b42874eb75
export BUILD_TAG=u24-release-8f60b04
BUILD_TYPE=release \
  CARGO_BUILD_FLAGS="--locked --features=testing" \
  make -j"$(nproc)" -s
```

默认构建 PG14-17、Neon PG extensions 和整个 Rust workspace。第一轮缩小验证可传 `POSTGRES_VERSIONS=v17`，但本轮最终构建覆盖了全部四个上游 PG major。

## 5. RPM 设计

首轮平台范围明确限制为 EL9 x86_64。不能据此宣称 EL8、EL10 或 aarch64 已验证。

生成的包：

- `neon`：pageserver、safekeeper、broker、controller、proxy、compute_ctl、neon_local、wrapper 和开发用 systemd unit。
- `neon-compute14`
- `neon-compute15`
- `neon-compute16`
- `neon-compute17`
- 对应 SRPM。

安装布局：

```text
/usr/bin/neon
/usr/bin/neon_local -> neon
/usr/libexec/neon/{pageserver,safekeeper,storage_broker,...}
/usr/lib64/neon/pg_install/v14
/usr/lib64/neon/pg_install/v15
/usr/lib64/neon/pg_install/v16
/usr/lib64/neon/pg_install/v17
/usr/lib/systemd/system/neon-local.service
/var/lib/neon
```

关键打包修复：

1. `port-allocation`：endpoint port 分配同时考虑 PG、external HTTP、internal HTTP，避免第二个 endpoint 端口重叠。
2. `snapshot-version`：没有 `.git` 时从 `vendor/revisions.json` 取得 PG submodule SHA。
3. `packaging`：提供 wrapper 与 dev/test systemd unit，并把 loopback 同时合入 `NO_PROXY`/`no_proxy`。
4. 三份 patch 都声明为 `PatchN` 并进入 SRPM；必须用 SRPM rebuild 验证，而不是依赖 builder 的 `SPECS/patches`。
5. Cargo dependency 由 vendor Source 提供，完全 offline/locked 构建。
6. PostgreSQL/PGXS 原本把临时 build prefix 写入 ELF RUNPATH。SPEC 用 `patchelf` 改为按位置区分的 `$ORIGIN`、`$ORIGIN/..`、`$ORIGIN/../lib`，保证每个 compute 使用自己随包提供的 `libpq.so.5`，不回落到系统 libpq。
7. 私有 PostgreSQL 库不对系统声明 provider，避免替代 PGDG 包或污染全局 ABI。

Builder 中准备并构建：

```bash
cd ~/rpmbuild
cp /path/to/neon-20260525.tar.gz SOURCES/
cp /path/to/neon-cargo-vendor-20260525.tar.gz SOURCES/
cp /path/to/protoc-25.1-linux-x86_64.zip SOURCES/
cp SPECS/patches/neon-20260525-*.patch SOURCES/

dnf builddep -y SPECS/neon.spec
rpmbuild -ba SPECS/neon.spec
```

SRPM 自包含验证：

```bash
rpm -qpl ~/rpmbuild/SRPMS/neon-*.src.rpm
rpmbuild --rebuild ~/rpmbuild/SRPMS/neon-*.src.rpm
```

## 6. 安装与本地完整链路

`neon_local` 是 dev/test 工具。初始化前不要直接 enable systemd unit：

```bash
dnf install -y \
  ./neon-compute14-*.rpm \
  ./neon-compute15-*.rpm \
  ./neon-compute16-*.rpm \
  ./neon-compute17-*.rpm \
  ./neon-20260525-*.rpm

runuser -u neon -- env HOME=/var/lib/neon \
  bash -lc 'cd /var/lib/neon && neon init'
runuser -u neon -- env HOME=/var/lib/neon \
  bash -lc 'cd /var/lib/neon && neon start'
runuser -u neon -- env HOME=/var/lib/neon \
  bash -lc 'cd /var/lib/neon && neon tenant create --set-default --pg-version 17'
runuser -u neon -- env HOME=/var/lib/neon \
  bash -lc 'cd /var/lib/neon && neon endpoint create main --pg-version 17'
runuser -u neon -- env HOME=/var/lib/neon \
  bash -lc 'cd /var/lib/neon && neon endpoint start main'
```

SQL/WAL smoke：

```bash
/usr/lib64/neon/pg_install/v17/bin/psql \
  -h 127.0.0.1 -p 55432 -U cloud_admin postgres <<'SQL'
CREATE TABLE smoke(id bigint PRIMARY KEY, payload text NOT NULL);
INSERT INTO smoke SELECT g, md5(g::text) FROM generate_series(1, 10000) g;
CHECKPOINT;
SELECT count(*), sum(id), sum(hashtext(payload)) FROM smoke;
SELECT current_setting('neon.timeline_id');
SQL
```

branch copy-on-write：

```bash
runuser -u neon -- env HOME=/var/lib/neon bash -lc \
  'cd /var/lib/neon && neon timeline branch --branch-name child'
runuser -u neon -- env HOME=/var/lib/neon bash -lc \
  'cd /var/lib/neon && neon endpoint create child --branch-name child --pg-version 17'
runuser -u neon -- env HOME=/var/lib/neon bash -lc \
  'cd /var/lib/neon && neon endpoint start child'
```

随后在 child 写入额外行，确认 child 为 11000 行、main 保持 10000 行；执行 endpoint stop/start 和整个 storage stack stop/start 后再次核对两边行数与 timeline ID。

初始化完成后，可以让 systemd **代替**手工 `neon start` 管理 storage stack。若前面已经手工启动，先执行 `neon stop`，再启用 unit：

```bash
runuser -u neon -- env HOME=/var/lib/neon \
  bash -lc 'cd /var/lib/neon && neon stop'
systemctl enable --now neon-local.service
```

`Type=oneshot + RemainAfterExit` 只管理 `neon start/stop` 生命周期，不监督任一 daemon，不适合作为生产服务管理方案。

## 7. 验证矩阵

最终交付前至少保存以下证据：

| 验证 | 目标 | 结果 |
|---|---|---|
| 上游源码 release build | Ubuntu 24.04 x86_64，PG14-17 | 通过；全部目标带 `git-env:8f60b04...`，PG 子模块版本正确 |
| Rust core unit tests | control_plane / safekeeper / storage_broker | 25 passed / 0 failed；这是 focused core subset，不是 workspace 全量 |
| pytest | u24 非 root，release-pg17 CLI basics + normal_work 两组参数 | 3 passed / 0 failed / 1 warning，27.53s；不是完整 pytest suite，teardown 有 pg_dynshmem 清理噪音，remote-storage 专项未跑 |
| source manual E2E | u24 PG17，SQL/WAL、`CREATE EXTENSION neon`、branch isolation、restart persistence | 通过；main `10000/50005000`，child `11000/60505500`，有序 stop/start 前后 timeline 与数据一致；未验证 crash/power-loss |
| RPM build | EL9 x86_64，无网络路由 | 通过；生成主包、compute14-17 和自包含 SRPM |
| SRPM rebuild | 独立真实 `_topdir`，无网络路由 | 通过；SRPM 内含 Source0/1/2、SPEC 和三份 patch；同 NEVRA 但 digest 不同，不是 bit-for-bit reproducible |
| clean RPM install E2E | direct-build RPM、无系统 `libpq`、PG17 | 通过；SQL、扩展、branch isolation、有序全栈重启，结束后无服务残留 |
| Vagrant clean VM acceptance | `mx`、libvirt/KVM、Rocky Linux 9.3 x86_64、5 个 canonical RPM | 通过；真实 systemd 启动、compute 重物化、storage stack restart、VM reboot persistence；VM 保持运行 |
| payload/ABI QA | rpm -qpl/-qRp、RUNPATH、private libpq、doc conflicts | 通过；PG14-17 均解析私有 libpq，无共享 `postgresql-doc-*` 冲突 |

Canonical EL9 x86_64 主包 SHA-256：

```text
b8571234d994c8d9cae43ea276bf0f23a034afde9223cd8ea0f0a6952afa393d
```

五个二进制包安装后约 581 MiB。SRPM 约 203 MiB，其中包含约 98 MiB 的离线 Cargo vendor Source。

运行时 E2E 仅覆盖 PG17；PG14-16 完成了编译、版本和私有链接 QA。Vagrant 验收已覆盖真实 systemd boot/reboot；`neon-local.service` 在启动成功后显示 `active (exited)` 是 `Type=oneshot + RemainAfterExit` 的预期行为，不表示 systemd 正在逐个监督 Neon daemon。最终 clean install 与 E2E 使用 direct-build RPM，没有对 SRPM rebuild 生成的第二组 RPM 再做一次安装态 E2E。

## 8. Vagrant 实机验收与使用

验收环境运行在 x86_64 主机 `mx`：Vagrant 2.4.9、`vagrant-libvirt` 0.12.2、libvirt/KVM，虚拟机配置为 8 vCPU、12 GiB RAM、128 GiB 根盘。固定使用 `generic/rocky9` 4.3.12 的 amd64/libvirt box；`rockylinux/9` 6.0.0 元数据指向已删除的 Rocky 9.6 `latest` 产物并返回 HTTP 404，因此没有使用。

box 的 SHA-256 为：

```text
17c5134c2972fbd01de9b06e9f2eaffaa3bf47ff4d480c946e3c0feab21f95fb
```

Rocky 9.3 box 自带 OpenSSH 8.7/OpenSSL 3.0，而当前仓库依赖事务会把 OpenSSL 升到 3.5；若不同时升级 OpenSSH，首次 reboot 会出现 `OpenSSL version mismatch` 并失去 SSH。provisioning 已在安装 Neon 前升级 `openssh`、`openssh-clients`、`openssh-server`，随后 enable/start `sshd.service`，并在 reboot 前显式检查。

当前通过验收的 VM 特意保持运行，可直接登录：

```bash
ssh mx
cd ~/neon-vagrant
vagrant status
vagrant ssh
```

guest 内查看 endpoint：

```bash
sudo runuser -u neon -- env HOME=/var/lib/neon \
  bash -c 'cd /var/lib/neon && neon endpoint list'
```

当前 PG17 endpoint：

| endpoint | port | timeline | SQL result |
|---|---:|---|---|
| `main` | 55432 | `13c5e2b4f28d7f5f8a2577f23f1f6896` | `10000/50005000` |
| `child` | 55435 | `e053a32a5931fe9fc98f03aa240959a9` | `11000/60505500` |

连接 main：

```bash
sudo /usr/lib64/neon/pg_install/v17/bin/psql \
  -h 127.0.0.1 -p 55432 -U cloud_admin postgres
```

独立复核当前运行态：

```bash
cd ~/neon-vagrant
vagrant rsync
vagrant ssh -c 'sudo bash /vagrant/verify-running.sh'
```

`./run-acceptance.sh` 面向干净 VM，使用固定 tenant、`main`、`child` 和验收状态文件，不设计成对同一数据目录重复执行。它验证：五个 RPM checksum/install、三项 storage health、SQL/WAL、COW branch isolation、compute stop 后 storage 继续健康、旧 PGDATA 哨兵在 start 时消失、storage stack restart，以及 VM reboot 后数据与 timeline 不变。日志保存在 `mx:~/neon-vagrant/logs/`；本轮副本已取回 `/Users/vonng/pgsty/deb/tmp/neon/results/logs/vagrant-el9/` 并通过 `SHA256SUMS` 复核。

## 9. “Serverless” 在这里如何实现

Serverless PostgreSQL 并不是“没有服务器”，而是把数据库的持久状态与某一台长期运行的 PostgreSQL 进程解绑，让控制面可以按需创建、停止、迁移和替换 compute。

这套 RPM 已具备 Serverless 的核心数据面机制：

1. **存算分离**：表页不以本地 `PGDATA` 为持久真源；compute 通过 Neon smgr 按 `GetPage@LSN` 从 pageserver 获取页面。
2. **WAL 独立持久化**：compute 的 walproposer 把 WAL 送到 safekeeper；pageserver 消费 WAL 并生成 immutable layer，生产形态再上传对象存储。
3. **compute 可丢弃**：`endpoint stop` 默认停止进程但保留 endpoint 目录；下一次 start 会删除旧 `pgdata`，由 `compute_ctl` 先同步 Safekeeper 状态，再从 Pageserver 下载 basebackup 并重新启动。表页由 Pageserver 提供，不是 compute 直接从 Safekeeper 读取。
4. **copy-on-write branch**：新 timeline 只记录祖先 LSN 与后续增量，不复制一整份数据库。本轮测试中 child 增加 1000 行后，main 仍保持原来的 10000 行。
5. **统一路由入口**：proxy/pg_sni_router 是未来把稳定连接地址映射到动态 endpoint 的入口；本轮编译了它们，但没有实现 Neon 云端私有控制面。

本地可以这样直接观察“compute scale-to-zero”的数据面效果：

```bash
# 只停止 compute；pageserver/safekeeper/controller 继续运行
runuser -u neon -- env HOME=/var/lib/neon \
  bash -lc 'cd /var/lib/neon && neon endpoint stop main'

# 此时不再有 main PostgreSQL compute 进程

# 按需重新拉起；旧 pgdata 会重建，数据和 timeline 不变
runuser -u neon -- env HOME=/var/lib/neon \
  bash -lc 'cd /var/lib/neon && neon endpoint start main'
```

当前 RPM **不会自动**在首个连接到来时唤醒 endpoint，也不会按空闲时间自动停止。要在 Pigsty 中形成真正的 Serverless 用户体验，需要增加控制面闭环：

```text
client
  -> always-on proxy
  -> endpoint state lookup
  -> stopped 时选择 compute host 并执行 endpoint start
  -> readiness 通过后转发/重试连接
  -> idle monitor 达到阈值后 endpoint stop

持久真源不在 compute：近期 WAL 由 Safekeeper quorum 保护，
物化后的 layer/metadata 进入对象存储；Pageserver 本地盘主要是工作集/cache
```

`neon_local` 默认仅使用单 Safekeeper，并以本地 filesystem 充当 remote storage，所以本轮只验证了功能链路和有序重启，不具备上述生产 HA/durability。此次交付证明了“compute 可启停并重新 materialize、数据不以 compute 为持久真源、分支不做全量复制”的 Serverless 基础；自动唤醒、空闲缩零、调度、计量、租户 API 和 HA 仍属于下一阶段 Pigsty 控制面工作。

## 10. Pigsty 生产集成缺口

RPM 能安装和跑通 `neon_local`，不等于 Pigsty 已获得 Neon 云服务能力。生产集成至少需要单独设计：

1. 角色拆分：pageserver、safekeeper、storage controller、broker、proxy、compute 分别建 role/service，而不是一个 oneshot unit。
2. Safekeeper quorum：至少三节点、跨故障域、成员变更与故障演练。
3. 对象存储：S3/MinIO 凭据、bucket/prefix 隔离、生命周期、恢复和灾备。
4. Controller HA：持久化 PostgreSQL、generation 一致性、leader/failover；不能使用 `neon_local` 的 `fsync=off` controller DB。
5. Compute 生命周期：创建、休眠、唤醒、扩缩容、镜像/extension 管理；这些云控制面不在 OSS `neon_local` 中。
6. Proxy routing：项目/endpoint 路由、认证、SNI、连接池；开源 proxy 不等于 Neon 云端完整 proxy。
7. 监控与运维：Prometheus、日志、磁盘水位、WAL backlog、layer upload、tenant attach、shard migration、升级与回滚。
8. PostgreSQL ABI：只能使用与该 Neon snapshot 对应的 patched PG14-17；Pigsty 的 vanilla PostgreSQL 包不能直接替换。
9. 扩展生态：Neon compute 的 extension payload、preload、升级与下载机制需要单独对齐 Pigsty extension catalog。
10. 平台矩阵：本轮没有验证 ARM64、EL8、EL10、Debian、Ubuntu 22/26，也没有做长期压力、故障注入或真实 S3 durability 测试。

## 11. 上游资料

- https://github.com/neondatabase/neon
- https://github.com/neondatabase/neon/blob/8f60b04da47ffefe0e52bda2440134b42874eb75/README.md
- https://github.com/neondatabase/neon/blob/8f60b04da47ffefe0e52bda2440134b42874eb75/docs/SUMMARY.md
- https://github.com/neondatabase/neon/blob/8f60b04da47ffefe0e52bda2440134b42874eb75/docs/walservice.md
- https://github.com/neondatabase/neon/blob/8f60b04da47ffefe0e52bda2440134b42874eb75/docs/storage_controller.md
- https://github.com/neondatabase/neon/blob/8f60b04da47ffefe0e52bda2440134b42874eb75/docs/core_changes.md
- https://github.com/neondatabase/neon/blob/8f60b04da47ffefe0e52bda2440134b42874eb75/control_plane/README.md
- https://github.com/neondatabase/neon/blob/8f60b04da47ffefe0e52bda2440134b42874eb75/docker-compose/README.md
- https://github.com/neondatabase/neon/releases/tag/release-9129
- https://neon.com/docs/introduction/architecture-overview
