# HAProxy RPM / DEB 打包契约

本规范适用于 Pigsty HAProxy 3.4 及之后的 RPM 与 DEB 包。目标是让两种包
具有相同的配置加载语义，同时保留发行版原生的用户、目录与服务生命周期
管理方式。

## 统一运行时契约

- 软件包安装主配置 `/etc/haproxy/haproxy.cfg`。
- 软件包创建并拥有空目录 `/etc/haproxy/conf.d`，但不放置占位 `.cfg`。
- HAProxy 始终先加载主配置，再加载配置目录：

  ```text
  -f /etc/haproxy/haproxy.cfg -f /etc/haproxy/conf.d
  ```

- systemd 启动命令与 reload 前校验必须使用同一组、同一顺序的 `-f` 参数；
  SysV 启动前校验、启动与 reload 也必须保持一致。
- `conf.d` 只使用非隐藏的 `*.cfg` 文件；文件名应带稳定的数字与所有者前缀。
- 主配置在 RPM 中是 `%config(noreplace)`，在 DEB 中是 conffile；包升级不得
  覆盖本地修改。
- RPM 与 DEB 都从当前 HAProxy 源码的 `admin/systemd/haproxy.service.in`
  生成 vendor unit，避免维护两份行为不同的手写 unit。

## 所有权边界

软件包拥有：

```text
/usr/sbin/haproxy
发行版原生 systemd vendor unit 路径中的 haproxy.service
/etc/haproxy/haproxy.cfg
/etc/haproxy/conf.d/
```

RPM 使用 sysusers 与 `/etc/sysconfig/haproxy`，并保持 chroot 根目录由
`root:root` 以 `0755` 拥有；DEB 使用 Debian maintainer scripts、tmpfiles
与 `/etc/default/haproxy`。这些实现差异不应改变配置加载语义。

Pigsty 或管理员拥有：

```text
/etc/haproxy/conf.d/*-pigsty-*.cfg
/etc/systemd/system/haproxy.service.d/*.conf
```

Pigsty 不应覆盖 vendor unit，也不应删除不属于 Pigsty 的配置片段。资源限制
等本地策略应通过最小 systemd drop-in 表达。

## 迁移约束

旧 Pigsty 把服务片段放在 `/etc/haproxy/*.cfg`，不属于本契约。迁移时必须先
创建并填充 `conf.d`，再用完整新参数校验。若存在旧 Pigsty 管理的
`/etc/systemd/system/haproxy.service`，编排层应在确认其所有权后删除该完整
override，执行 `systemctl daemon-reload`，让系统重新使用软件包的 vendor
unit；软件包自身不能安全删除管理员文件。

HAProxy master-worker 收到 `SIGUSR2` 后会复用当前进程的 argv；从旧加载参数
切换到新参数时，因此需要一次受控 restart。完成切换后的日常 reload 仍使用
HAProxy 的无损重载流程。

RPM 的上游生成 unit 使用 `EXTRAOPTS`；旧 PGDG 风格的 `OPTIONS` 不再是
受支持接口。迁移前应检查 `/etc/sysconfig/haproxy`，把仍需保留的参数显式
迁移到 `EXTRAOPTS`。

HAProxy 3.4 提供运行时参数 `tune.stick-counters`。旧 RPM 曾在编译期把
`MAX_SESS_STKCTR` 改为 12；新版恢复上游默认 3。仍使用 `track-sc3` 及以上
规则的配置，应在 `global` 中显式设置 `tune.stick-counters 12`（或实际所需
值）后再升级。

EL8 的旧 systemd RPM 宏可能在事务末尾 daemon-reload 之前先按旧 unit
restart。因此，从旧加载参数迁移时，单独执行 `dnf update` 不算完成迁移；
仍须按本节顺序执行 daemon-reload、完整校验和受控 restart。

软件包不自动搬运或删除旧服务片段、管理员 unit override，也不在升级脚本中
擅自重写管理员配置。

## 最小验收

1. RPM 与 DEB payload 都包含空的 `/etc/haproxy/conf.d`。
2. 两种包的 vendor unit 都由同版本源码生成，并加载 `haproxy.cfg + conf.d`。
3. 启动与 reload 校验的配置集合完全一致；SysV 三条路径也完全一致。
4. 主配置升级后保留；管理员 drop-in 不被软件包覆盖。
5. 合法主配置与合法片段可通过 `haproxy -c`；无效片段会阻止 reload。
6. 构建产物显示预期的 OpenSSL、PCRE2 JIT、Lua、SLZ、QUIC 与 PROMEX 特性。

RPM 构建应使用非 PostgreSQL 版本化的专用目标，避免重复构建同一产物。源码
镜像与 spec 同步后，常规流程必须按真实文件名显式获取两个输入：

```bash
cd ~/rpmbuild
pig build get -f \
  haproxy-3.4.3.tar.gz haproxy-utils.tar.gz
make haproxy
```

`haproxy-utils.tar.gz` 使用 GNU tar 确定性生成，固定文件顺序、所有者、时间戳和
gzip header，并包含 RPM 所需的五个发行版集成文件：

```text
haproxy-utils/haproxy.cfg
haproxy-utils/haproxy.logrotate
haproxy-utils/haproxy.sysconfig
haproxy-utils/halog.1
haproxy-utils/haproxy-sysusers.conf
```

`pig build get haproxy` 会请求一个字面名称为 `haproxy` 的文件，不是这个
recipe 的有效获取命令。`-f` 也只应在公共源码镜像已经同步并核验后使用。

在新版源码镜像正式同步之前，公共镜像仍可能返回旧版辅助归档或缺少 3.4.3
tarball。此时不能混用公共镜像输入；必须从本地权威目录复制这两个文件，而不
是同步整个 `src`：

```bash
cp ~/pgsty/repo/ext/src/{haproxy-3.4.3.tar.gz,haproxy-utils.tar.gz} \
  ~/rpmbuild/SOURCES/
```

RPM spec 在 `%prep` 对两个输入做固定 SHA-256 校验；DEB recipe 在解包前校验
上游 tarball。3.4.3 官方 tarball 与 RPM 辅助归档的 SHA-256 分别是：

```text
7fa666d36d198275999e2a68dda44d3d37960f2f7aed3a595fb811f4fd0515b5
08fea6dc7c1e62fa0acfe0eeee07e6202fee84338b49fab220066c4fcdff916d
```

因此，过期、混合或被意外改写的镜像输入必须让构建失败，而不是静默产生错误
包。源码镜像发布与二进制仓库签名、索引、上传是两个独立发布阶段。

## 发布迁移

已发布的 3.4.2 DEB 使用旧服务契约。正式发布 3.4.3 时，当前支持的
`jammy`、`bookworm`、`noble`、`trixie`、`resolute` 必须用新包覆盖旧包；
已经移出当前构建矩阵的 `focal` 与 `bullseye` 则必须明确撤回旧包，或走单独
兼容修复，不能继续把旧 3.4.2 当作可用版本。本次 recipe 修改不执行签名、
索引、上传、覆盖或撤回操作。
