# 非 Rust SPEC 与补丁审查 — 2026-11-21

本轮完成 RPM / DEB 工作树内本批变更的逐项审查与拆分提交。按源码构建单元归并子包，共 **347 个单元、626 个扩展/组件提交：RPM 321、DEB 305**。两仓库各有一个公共构建编排提交；审查文档另行提交。未改动的配方不制造空提交。

全量盘点为 478 个源码单元，其中 403 个非 Rust 单元；75 个 Rust 单元冻结，9 个大型单元和 18 个内核单元后置。本轮审查延续这一范围。默认目标为 PG15–19，逐扩展采用实际支持子集，PG14 与 EL8 退出默认构建。

- [完整版本与 PG15–19 矩阵](nonrust-pg19-20261121.json)
- [初轮核验记录](nonrust-pg19-20261121.md)
- [交互式审查 HTML](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/nonrust-spec-review-20261121.html)
- [完整兼容矩阵 HTML](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/nonrust-pg19-final-report.html)
- [原始审查与提交账本](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/final-review.json)

## 修正结果

| 对象 | 问题与审查结论 | 实际处理与验证 |
|---|---|---|
| mongo_fdw | 系统库补丁曾将 legacy Extended JSON 改为 relaxed JSON，日期和 binary 输出会改变 | 使用 libbson/mongoc <1.30 的兼容别名保持上游 legacy 语义；命名为 `mongo_fdw-5.5.3-system-libraries.patch`。两侧 PG18/19 重建验包通过，并以生产源码中的函数验证对象/数组的 date、binary 输出。外部 MongoDB 服务端到端路径未覆盖。 |
| ulak | compat 补丁混入当前目标平台不需要的 libcurl <7.66 fallback | 仅保留 EL9 hiredis 1.0 的 keepalive API 兼容，命名为 `ulak-0.3.0-hiredis-keepalive.patch`；两侧 PG19 重建验包通过。PG19 numeric 非抛错错误处理补丁继续保留。 |
| pg_datasentinel、pg_failover_slots、pg_variables | PG19 候选仅解决编译层，功能/回归未验收 | 从两侧正式应用链撤出三个 PG19 候选，PG19 继续禁用。撤出后 PG18 两侧重建验包通过；既有 PG18/19 功能问题仍保留，未据此宣称回归已通过。候选归档在仓库外。 |
| pg_variables | composite datum 安全修复与 PG19 候选应独立判断 | 保留 core tuple-copy API 修复，改名为 `pg_variables-1.2.5-composite-datum.patch`，保留 PG15–18 小版本下限；合并 DEB 本轮重复 changelog。 |
| pgactive / DEB | Build-Depends 的 PG security minor 下限未进入运行时 Depends | 在 `override_dh_gencontrol` 设置适用下限。新 PG18/19 包实际要求 `postgresql-18 (>= 18.7)`、`postgresql-19 (>= 19.0)`，均完成构建、payload 和 dbgsym 验证。 |
| pg_datasentinel / RPM | LLVM22 编译的 bitcode 由 LLVM21 ThinLTO 读取，安装阶段失败 | 对齐 `LLVM_BINPATH=%{_bindir}`，保持 LLVM 启用；PG18 重建通过。保留最初失败日志与准确首错。 |
| 307 个生成 control | 本轮生成的 `debian/control` 均有 `control.in`，不应作为新的 recipe 真源提交 | 已移至仓库外审查归档；已有 Git 跟踪的 control 保留，没有用宽泛 ignore 掩盖未来文件。 |

## 补丁判定方法与命名

按内容去重共 57 项：**50 保留、2 修正后保留、3 撤出暂缓、2 由上游替代且不纳入提交**。后两份旧 pg_uint128 大补丁没有作为当前适用补丁全文重审；保留用户原文件，不纳入本轮提交。

每项核对目标 API/工具链变化与首次错误、实际调用路径、旧版本分支、声明与委派的一致性、补丁应用位置和真实构建输入。单一用途命名采用 `<extension>-<version>-<purpose>.patch`；只有多个相关 API 变化才保留 `pg19-compat`。已有 Debian quilt 的 `target-server-headers.patch` 沿用该项目局部命名。

仅更名或修正说明的补丁逐字节核对 unified diff 主体，包括 zhparser 的 CRLF；RPM/DEB 共同补丁一致。mongo_fdw、ulak 的实质改动分别记录并重建。构建通过只支持构建层结论，充分性的运行边界按以下证据逐项记录。

## 验证范围

- **静态解析**：EL9a 上 287 个变动 RPM spec 按支持子集展开；m3/u24 上 305 个 DEB recipe 解析 Makefile 并生成 control。检查结果均无错误。RPM 的 321 个提交还包括只调整构建 target 的单元，因此与 287 个 spec 数量不同。
- **本轮新增构建**：Rocky Linux 9.8 / aarch64 / `pgsty/el9a:build` 成功 6 次；Ubuntu 24.04.5 noble / amd64 / m3 / `pgsty/u24:build` 成功 8 次。另有 1 次已解决的 LLVM 失败。逐项核对构建输入：79 个文件 SHA256 完全一致，6 项差异只涉及补丁说明或 changelog 文案；已从 builder 取回原输入并证明 diff 主体、构建配方与版本不变。
- **payload/debug**：14 次成功构建均验包；原生 RPM 包含非空 debuginfo、debugsource，DEB 包含 dbgsym。LLVM 保持开启，主包 bitcode 与依赖检查有独立 QA 记录。
- **语义测试**：两侧以实际应用补丁后的 mongo_fdw 函数验证 JSON 对象、数组中的 date 与 binary，与 legacy 输出一致；未覆盖外部 MongoDB 服务。
- **公共编排**：9 次 shell 解析与 Makefile dry-run 检查通过；RPM 剩余 57 处构建命令只删除 PG14（含删除 libpgfeutils14 命令），冻结/后置目标未获得 PG19。
- **证据复用**：初轮 981 次构建尝试与原有运行/回归记录继续保留。本轮没有重跑全部 PG15–19 或全部生产平台，不把继承证据当作本轮新测试。

### 新增构建记录

| 平台 | 扩展 | PG | 结果 | 产物数 | 证据 |
|---|---|---|---|---:|---|
| deb / amd64 | mongo_fdw | 18 | 构建 + 验包通过 | 2 | [receipt](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-mongo_fdw-pg18.json) · [QA](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-mongo_fdw-pg18.qa.json) |
| deb / amd64 | mongo_fdw | 19 | 构建 + 验包通过 | 2 | [receipt](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-mongo_fdw-pg19.json) · [QA](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-mongo_fdw-pg19.qa.json) |
| deb / amd64 | pg_datasentinel | 18 | 构建 + 验包通过 | 2 | [receipt](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-pg_datasentinel-pg18.json) · [QA](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-pg_datasentinel-pg18.qa.json) |
| deb / amd64 | pg_failover_slots | 18 | 构建 + 验包通过 | 2 | [receipt](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-pg_failover_slots-pg18.json) · [QA](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-pg_failover_slots-pg18.qa.json) |
| deb / amd64 | pg_variables | 18 | 构建 + 验包通过 | 2 | [receipt](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-pg_variables-pg18.json) · [QA](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-pg_variables-pg18.qa.json) |
| deb / amd64 | pgactive | 18 | 构建 + 验包通过 | 2 | [receipt](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-pgactive-pg18.json) · [QA](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-pgactive-pg18.qa.json) |
| deb / amd64 | pgactive | 19 | 构建 + 验包通过 | 2 | [receipt](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-pgactive-pg19.json) · [QA](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-pgactive-pg19.qa.json) |
| deb / amd64 | ulak | 19 | 构建 + 验包通过 | 2 | [receipt](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-ulak-pg19.json) · [QA](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-ulak-pg19.qa.json) |
| rpm / aarch64 | mongo_fdw | 18 | 构建 + 验包通过 | 3 | [receipt](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-mongo_fdw-pg18.json) · [QA](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-mongo_fdw-pg18.qa.json) |
| rpm / aarch64 | mongo_fdw | 19 | 构建 + 验包通过 | 3 | [receipt](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-mongo_fdw-pg19.json) · [QA](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-mongo_fdw-pg19.qa.json) |
| rpm / aarch64 | pg_datasentinel | 18 | 构建 + 验包通过 | 3 | [receipt](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-pg_datasentinel-pg18.json) · [QA](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-pg_datasentinel-pg18.qa.json) |
| rpm / aarch64 | pg_failover_slots | 18 | 构建 + 验包通过 | 3 | [receipt](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-pg_failover_slots-pg18.json) · [QA](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-pg_failover_slots-pg18.qa.json) |
| rpm / aarch64 | pg_variables | 18 | 构建 + 验包通过 | 3 | [receipt](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-pg_variables-pg18.json) · [QA](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-pg_variables-pg18.qa.json) |
| rpm / aarch64 | ulak | 19 | 构建 + 验包通过 | 3 | [receipt](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-ulak-pg19.json) · [QA](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-ulak-pg19.qa.json) |

LLVM 首错：`LLVM ERROR: ThinLTO cannot create input file: Unknown attribute kind (105) (Producer: 'LLVM22.1.8' Reader: 'LLVM 21.1.8')`，见 [失败日志第 67 行](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-pg_datasentinel-pg18.failed-llvm.log:67)。失败 receipt 已指向保留的 failed-llvm 日志；原始包装层错误另存字段，没有被成功重跑覆盖。

## 未扩大验收的边界

PG19 的 `local_recipe_integrated` 仅表示已纳入配方。`payload-passed`、冒烟通过、部分回归、差异复核和完整回归分开记录。pg_datasentinel、pg_failover_slots、pg_variables 的 PG19 功能/回归阻塞继续有效。旧版本构建通过不消除已有运行失败。

此前按用户授权完成的 PGEXT `extension` / `universe` 元数据更新有独立回执：包版本字段分别涉及 40 / 42 行；数据库与导出 CSV 核对通过。本轮 spec 审查没有再次修改 PGEXT，也没有提交其现有工作树。

未执行生产矩阵、staging/stash、签名、仓库/CDN 发布或 Git push。用户原有 `openhalodb-18.spec` 改动和两侧旧 pg_uint128 1.2.0 大补丁保留在工作树中。本机 RPM SOURCES 保持为空。

## 逐项补丁审查

### 01. aggs_for_vecs — 保留

- 原名：`aggs_for_vecs-1.4.1-pg19-numeric.patch`。
- 当前/归档名称：`aggs_for_vecs-1.4.1-pg19-numeric.patch`。
- 必要性：PG19 numeric optional-error API 被替换。
- 最小性：仅在 PG19 映射四个 numeric API；所有调用均传 NULL，保留原有 ERROR 语义。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/aggs_for_vecs-1.4.1-pg19-numeric.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/aggs_for_vecs/patches/aggs_for_vecs-1.4.1-pg19-numeric.patch)。
- rpm PG19：`regression-reviewed-differences`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/batch01-fix/rpm/aggs_for_vecs.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-utf8-rpm-19.json)。
- deb PG19：`regression-reviewed-differences`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/batch01-fix/deb/aggs_for_vecs.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-utf8-deb-19.json)。

### 02. codesystem — 保留

- 原名：`codesystem-0.2.1-pg19-c11.patch`。
- 当前/归档名称：`codesystem-0.2.1-pg19-c11.patch`。
- 必要性：PG19 头文件要求 C11 特性。
- 最小性：仅将编译方言从 C99 改为 GNU11。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/codesystem-0.2.1-pg19-c11.patch)。
- rpm PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/batch01-fix/rpm/codesystem.json)。
- deb PG19：`no-local-recipe`；PG19 配方未启用。

### 03. datasketches — 保留

- 原名：`datasketches-1.7.0-pg19-compat.patch`。
- 当前/归档名称：`datasketches-1.7.0-pg19-datum-pointers.patch`。
- 必要性：PG19 varlena accessor 需要指针实参。
- 最小性：四处 DatumGetPointer 转换，保持输入字节和 sketch 算法。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/datasketches-1.7.0-pg19-datum-pointers.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/datasketches/patches/datasketches-1.7.0-pg19-datum-pointers.patch)。
- rpm PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/packaging03-fix/rpm/datasketches.json)。
- deb PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/packaging03-fix/deb/datasketches.json)。

### 04. decoderbufs — 保留

- 原名：`decoderbufs-3.7.1-pg19-compat.patch`。
- 当前/归档名称：`decoderbufs-3.7.1-pg19-compat.patch`。
- 必要性：输出插件类型断言、时间戳 union 和 varlena API 变化。
- 最小性：保留编译期 callback 检查；版本条件限定时间戳访问，显式 Datum 转换并选择 GNU11。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/decoderbufs-3.7.1-pg19-compat.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/decoderbufs/patches/decoderbufs-3.7.1-pg19-compat.patch)。
- rpm PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/upgrade02-fix2/rpm/decoderbufs.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-functional-v2-rpm-19.json)。
- deb PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/upgrade02-fix2/deb/decoderbufs.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-functional-v2-deb-19.json)。

### 05. hashtypes — 保留

- 原名：`hashtypes-0.1.5-pg19-compat.patch`。
- 当前/归档名称：`hashtypes-0.1.5-pg19-varlena.patch`。
- 必要性：SET_VARSIZE 在 PG19 是 inline 函数，旧宏检测会错误启用 fallback。
- 最小性：移除依赖已删除 VARATT_SIZEP 的过时 fallback；所有目标版本已有 SET_VARSIZE。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/hashtypes-0.1.5-pg19-varlena.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/hashtypes/patches/hashtypes-0.1.5-pg19-varlena.patch)。
- rpm PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01/rpm/hashtypes.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-utf8-rpm-19.json)。
- deb PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01-deb/deb/hashtypes.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-utf8-deb-19.json)。

### 06. jdbc_fdw — 保留

- 原名：`jdbc_fdw-0.5.0-pg19-compat.patch`。
- 当前/归档名称：`jdbc_fdw-0.5.0-pg19-compat.patch`。
- 必要性：元组声明不再间接引入，varlena 参数类型变化。
- 最小性：仅补元组头文件及 DatumGetPointer，保留 JDBC 数据转换流程。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/jdbc_fdw-0.5.0-pg19-compat.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/jdbc_fdw/debian/patches/jdbc_fdw-0.5.0-pg19-compat.patch)。
- rpm PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api07/rpm/jdbc_fdw.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-jdbc-rpm-19.json)。
- deb PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/jdbc-runtime/deb/jdbc_fdw.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-jdbc-fixed-deb-19.json)。

### 07. kafka_fdw — 保留

- 原名：`kafka_fdw-0.0.3-pg19-compat.patch`。
- 当前/归档名称：`kafka_fdw-0.0.3-pg19-tuplestore.patch`。
- 必要性：tuplestore 声明不再间接引入。
- 最小性：单一 include。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/kafka_fdw-0.0.3-pg19-tuplestore.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/kafka_fdw/patches/kafka_fdw-0.0.3-pg19-tuplestore.patch)。
- rpm PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01/rpm/kafka_fdw.json)。
- deb PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01-deb/deb/kafka_fdw.json)。

### 08. logical_ddl — 保留

- 原名：`logical_ddl-0.1.0-pg19-compat.patch`。
- 当前/归档名称：`logical_ddl-0.1.0-pg19-compat.patch`。
- 必要性：tuplestore 声明缺失、bits16 别名移除。
- 最小性：显式头文件和同宽 uint16 替代。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/logical_ddl-0.1.0-pg19-compat.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/logical_ddl/patches/logical_ddl-0.1.0-pg19-compat.patch)。
- rpm PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers02/rpm/logical_ddl.json)。
- deb PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers02/deb/logical_ddl.json)。

### 09. macavity — 保留

- 原名：`macavity-0.2.0-pg19-compat.patch`。
- 当前/归档名称：`macavity-0.2.0-pg19-headers.patch`。
- 必要性：元组和 tuplestore 声明不再间接引入。
- 最小性：两个必要头文件。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/macavity-0.2.0-pg19-headers.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/macavity/patches/macavity-0.2.0-pg19-headers.patch)。
- rpm PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01/rpm/macavity.json)。
- deb PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01-deb/deb/macavity.json)。

### 10. mobilitydb — 保留

- 原名：`mobilitydb-1.3.2-pg19-headers.patch`。
- 当前/归档名称：`mobilitydb-1.3.2-pg19-headers.patch`。
- 必要性：math、tuple 声明缺失，varlena inline 参数收紧。
- 最小性：仅补使用位置的头文件及 Datum 指针转换；没有改动空间运算。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/mobilitydb-1.3.2-pg19-headers.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/mobilitydb/debian/patches/mobilitydb-1.3.2-pg19-headers.patch)。
- rpm PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api06-followup/rpm/mobilitydb.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api08-corrected-rpm-19.json)。
- deb PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api06-followup/deb/mobilitydb.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api08-corrected-deb-19.json)。

### 11. mobilitydb — 保留

- 原名：`mobilitydb-1.3.2-preserve-geometry-input.patch`。
- 当前/归档名称：`mobilitydb-1.3.2-preserve-geometry-input.patch`。
- 必要性：共享 geometry 输入被原地修改。
- 最小性：采用已记录上游 commit 的输入保留修复；验证覆盖 geometry 输入与 composite 返回，未重写空间算法。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/mobilitydb-1.3.2-preserve-geometry-input.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/mobilitydb/debian/patches/mobilitydb-1.3.2-preserve-geometry-input.patch)。
- rpm PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api06-followup/rpm/mobilitydb.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api08-corrected-rpm-19.json)。
- deb PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api06-followup/deb/mobilitydb.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api08-corrected-deb-19.json)。

### 12. mongo_fdw — 保留

- 原名：`mongo_fdw-5.5.3-pg19-compat.patch`。
- 当前/归档名称：`mongo_fdw-5.5.3-pg19-compat.patch`。
- 必要性：上游版本门禁、C99 和 math 声明阻碍 PG19 编译。
- 最小性：仅放行已验证 PG19、使用 GNU11、补 math.h。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/mongo_fdw-5.5.3-pg19-compat.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/mongo_fdw/debian/patches/mongo_fdw-5.5.3-pg19-compat.patch)。
- rpm PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/mongo-headers/rpm/mongo_fdw.json)。
- deb PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/mongo-headers/deb/mongo_fdw.json)。
- deb PG18：`passed`；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-mongo_fdw-pg18.json)。
- deb PG19：`passed`；PG19 配方未启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-mongo_fdw-pg19.json)。
- rpm PG18：`passed`；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-mongo_fdw-pg18.json)。
- rpm PG19：`passed`；PG19 配方未启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-mongo_fdw-pg19.json)。

### 13. mongo_fdw — 修正后保留

- 原名：`mongo_fdw-5.5.3.patch`。
- 当前/归档名称：`mongo_fdw-5.5.3-system-libraries.patch`。
- 必要性：使用系统 MongoDB/json-c；1.28 缺少 1.30 重命名的 API。
- 最小性：删掉改变 JSON 格式的 relaxed 路径；以版本条件别名映射 legacy API。日期和 binary 的对象/数组表示在两侧验证一致。
- 充分性与边界：验证 legacy JSON 转换及 PG18/19 包产物；未声称已完成外部 MongoDB 服务的端到端测试。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/mongo_fdw-5.5.3-system-libraries.patch)。
- rpm PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/mongo-headers/rpm/mongo_fdw.json)。
- deb PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/mongo-headers/deb/mongo_fdw.json)。
- deb PG18：`passed`；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-mongo_fdw-pg18.json)。
- deb PG19：`passed`；PG19 配方未启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-mongo_fdw-pg19.json)。
- rpm PG18：`passed`；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-mongo_fdw-pg18.json)。
- rpm PG19：`passed`；PG19 配方未启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-mongo_fdw-pg19.json)。

### 14. omnisketch — 保留

- 原名：`omnisketch-1.0.2-pg19-compat.patch`。
- 当前/归档名称：`omnisketch-1.0.2-pg19-headers.patch`。
- 必要性：元组与 varlena 声明缺失。
- 最小性：补 tuple 头文件；varatt.h 以 PG16 起可用为条件，保留 PG15。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/omnisketch-1.0.2-pg19-headers.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/omnisketch/patches/omnisketch-1.0.2-pg19-headers.patch)。
- rpm PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01/rpm/omnisketch.json)。
- deb PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01-deb/deb/omnisketch.json)。

### 15. permuteseq — 保留

- 原名：`permuteseq-1.2.2-pg19-compat.patch`。
- 当前/归档名称：`permuteseq-1.2.2-pg19-tuple-header.patch`。
- 必要性：元组声明不再间接引入。
- 最小性：单一 include。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/permuteseq-1.2.2-pg19-tuple-header.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/permuteseq/patches/permuteseq-1.2.2-pg19-tuple-header.patch)。
- rpm PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01/rpm/permuteseq.json)。
- deb PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01-deb/deb/permuteseq.json)。

### 16. pg_arraymath — 保留

- 原名：`pg_arraymath-1.1-pg19-compat.patch`。
- 当前/归档名称：`pg_arraymath-1.1-pg19-compat.patch`。
- 必要性：PG19 声明与别名变化；PG18 core array_sort 会抢占内部符号调用。
- 最小性：增加必要头文件、uint8 和 static 内部 sort helper；保留 SQL 入口，回归只限定实际要测试的 public 函数。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pg_arraymath-1.1-pg19-compat.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pg_arraymath/patches/pg_arraymath-1.1-pg19-compat.patch)。
- rpm PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/arraymath-fix/rpm/pg_arraymath.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-arrayfixed-rpm-19.json)。
- deb PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/arraymath-fix/deb/pg_arraymath.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-compat-deb-19.json)。

### 17. pg_bzip — 保留

- 原名：`pg_bzip-1.0.0-pg19-compat.patch`。
- 当前/归档名称：`pg_bzip-1.0.0-pg19-varatt-header.patch`。
- 必要性：varlena 声明不再间接引入。
- 最小性：按 PG16 版本边界引入 varatt.h。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pg_bzip-1.0.0-pg19-varatt-header.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pg_bzip/patches/pg_bzip-1.0.0-pg19-varatt-header.patch)。
- rpm PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01/rpm/pg_bzip.json)。
- deb PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01-deb/deb/pg_bzip.json)。

### 18. pg_datasentinel — 撤出并暂缓

- 原名：`pg_datasentinel-1.0-pg19-compat.patch`。
- 候选已退出正式应用链，归档名称：`pg_datasentinel-1.0-pg19-compat.patch`。
- 归档文件：[rpm](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/deferred-patches/rpm/rpmbuild/SPECS/patches/pg_datasentinel-1.0-pg19-compat.patch) · [deb](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/deferred-patches/deb/debbuild/pg_datasentinel/debian/patches/pg_datasentinel-1.0-pg19-compat.patch)。
- 必要性：PG19 log_min_messages 变为按 backend 索引的数组。
- 最小性：候选只能解决编译层；既有功能/回归失败未解决，从正式应用链撤出，保留补丁与失败记录。
- 充分性与边界：PG19 继续禁用；PG18 撤出候选后的构建/验包通过，不覆盖此前已记录的功能问题。
- rpm PG19：`functional-failed`；PG19 配方未启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api05-headers/rpm/pg_datasentinel.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-datasentinel-rpm-19.json)。
- deb PG19：`functional-failed`；PG19 配方未启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api05-quilt/deb/pg_datasentinel.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-datasentinel-deb-19.json)。
- deb PG18：`passed`；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-pg_datasentinel-pg18.json)。
- rpm PG18：`build-failed`；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-pg_datasentinel-pg18.failed-llvm.json)。
- rpm PG18：`passed`；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-pg_datasentinel-pg18.json)。

### 19. pg_describe — 保留

- 原名：`pg_describe-1.0.0-pg19-compat.patch`。
- 当前/归档名称：`pg_describe-1.0.0-pg19-tuplestore.patch`。
- 必要性：tuplestore 声明不再间接引入。
- 最小性：单一 include。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pg_describe-1.0.0-pg19-tuplestore.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pg_describe/patches/pg_describe-1.0.0-pg19-tuplestore.patch)。
- rpm PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01/rpm/pg_describe.json)。
- deb PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01-deb/deb/pg_describe.json)。

### 20. pg_disorder — 保留

- 原名：`pg_disorder-0.1.0-pg19-compat.patch`。
- 当前/归档名称：`pg_disorder-0.1.0-pg19-compat.patch`。
- 必要性：PG19 planner_hook 新增 ExplainState。
- 最小性：补 tuple 头文件，并在 callback 和两个委派路径完整传递 es。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pg_disorder-0.1.0-pg19-compat.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pg_disorder/debian/patches/pg_disorder-0.1.0-pg19-compat.patch)。
- rpm PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api05-headers/rpm/pg_disorder.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api05-rpm-19.json)。
- deb PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api05-quilt/deb/pg_disorder.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api05-deb-19.json)。

### 21. pg_failover_slots — 撤出并暂缓

- 原名：`pg_failover_slots-1.2.1-pg19-compat.patch`。
- 候选已退出正式应用链，归档名称：`pg_failover_slots-1.2.1-pg19-compat.patch`。
- 归档文件：[rpm](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/deferred-patches/rpm/rpmbuild/SPECS/patches/pg_failover_slots-1.2.1-pg19-compat.patch) · [deb](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/deferred-patches/deb/debbuild/pg_failover_slots/patches/pg_failover_slots-1.2.1-pg19-compat.patch)。
- 必要性：PG19 复制槽 API 和状态字段变化。
- 最小性：候选未通过功能/回归验收，撤出正式应用链；同时记录其机械改名误改注释的问题。
- 充分性与边界：PG19 继续禁用；PG18 撤出候选后的构建/验包通过，不覆盖此前已记录的功能问题。
- rpm PG19：`regression-failed`；PG19 配方未启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api05/rpm/pg_failover_slots.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api05-rpm-19.json)。
- deb PG19：`regression-failed`；PG19 配方未启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api05/deb/pg_failover_slots.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api05-deb-19.json)。
- deb PG18：`passed`；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-pg_failover_slots-pg18.json)。
- rpm PG18：`passed`；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-pg_failover_slots-pg18.json)。

### 22. pg_kpart — 保留

- 原名：`pg_kpart-1.0-pg19-compat.patch`。
- 当前/归档名称：`pg_kpart-1.0-pg19-planner-hook.patch`。
- 必要性：PG19 planner_hook 新增 ExplainState。
- 最小性：只在 PG19 callback 和委派调用中增加 es。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pg_kpart-1.0-pg19-planner-hook.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pg_kpart/debian/patches/pg_kpart-1.0-pg19-planner-hook.patch)。
- rpm PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api06/rpm/pg_kpart.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api06-rpm-19.json)。
- deb PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api06/deb/pg_kpart.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api06-deb-19.json)。

### 23. pg_local_cache — 保留

- 原名：`pg_local_cache-3.1.0-pg19-compat.patch`。
- 当前/归档名称：`pg_local_cache-3.1.0-pg19-compat.patch`。
- 必要性：PG19 ShmemInitHash 移除 initial-size 参数。
- 最小性：旧版的 initial/max 原本相同，仅按版本省略一个参数，保持固定容量。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pg_local_cache-3.1.0-pg19-compat.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pg_local_cache/debian/patches/pg_local_cache-3.1.0-pg19-compat.patch)。
- rpm PG19：`partial-regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api07/rpm/pg_local_cache.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-localcache-admin-rpm-19.json)。
- deb PG19：`partial-regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api07/deb/pg_local_cache.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-localcache-admin-deb-19.json)。

### 24. pg_nanotime — 保留

- 原名：`pg_nanotime-0.3.0-pg19-compat.patch`。
- 当前/归档名称：`pg_nanotime-0.3.0-pg19-tuple-header.patch`。
- 必要性：元组声明不再间接引入。
- 最小性：单一 include。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pg_nanotime-0.3.0-pg19-tuple-header.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pg_nanotime/patches/pg_nanotime-0.3.0-pg19-tuple-header.patch)。
- rpm PG19：`regression-reviewed-differences`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01/rpm/pg_nanotime.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-utf8-rpm-19.json)。
- deb PG19：`regression-reviewed-differences`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01-deb/deb/pg_nanotime.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-utf8-deb-19.json)。

### 25. pg_plan_filter — 保留

- 原名：`pg_plan_filter-1.0.0-pg19-compat.patch`。
- 当前/归档名称：`pg_plan_filter-1.0.0-pg19-planner-hook.patch`。
- 必要性：PG19 planner_hook 新增 ExplainState。
- 最小性：声明、定义、previous hook 与 standard_planner 调用同步，保留旧版签名。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pg_plan_filter-1.0.0-pg19-planner-hook.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pg_plan_filter/debian/patches/pg_plan_filter-1.0.0-pg19-planner-hook.patch)。
- rpm PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api06/rpm/pg_plan_filter.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api06-rpm-19.json)。
- deb PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api06/deb/pg_plan_filter.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api06-deb-19.json)。

### 26. pg_qos — 保留

- 原名：`pg_qos-1.1.0-pg19-compat.patch`。
- 当前/归档名称：`pg_qos-1.1.0-pg19-compat.patch`。
- 必要性：PG19 planner_hook 新增 ExplainState。
- 最小性：跨 wrapper 与 callback 保留完整 es 传递，版本条件覆盖所有边界。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pg_qos-1.1.0-pg19-compat.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pg_qos/debian/patches/pg_qos-1.1.0-pg19-compat.patch)。
- rpm PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api06/rpm/pg_qos.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api08-corrected-rpm-19.json)。
- deb PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api06/deb/pg_qos.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api08-corrected-deb-19.json)。

### 27. pg_savior — 保留

- 原名：`pg_savior-0.1.0-pg19-compat.patch`。
- 当前/归档名称：`pg_savior-0.1.0-pg19-compat.patch`。
- 必要性：PG19 post-parse hook 使用 const JumbleState，limits 声明缺失。
- 最小性：仅匹配 callback constness 并引入 limits.h。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pg_savior-0.1.0-pg19-compat.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pg_savior/patches/pg_savior-0.1.0-pg19-compat.patch)。
- rpm PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01/rpm/pg_savior.json)。
- deb PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01-deb/deb/pg_savior.json)。

### 28. pg_similarity — 保留

- 原名：`pg_similarity-1.0-pg19-compat.patch`。
- 当前/归档名称：`pg_similarity-1.0-pg19-uint8.patch`。
- 必要性：PG19 删除 bits8。
- 最小性：用同宽 uint8 替换两处指针声明，算法保持不变。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pg_similarity-1.0-pg19-uint8.patch)。
- rpm PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01/rpm/pg_similarity.json)。
- deb PG19：`no-local-recipe`；PG19 配方未启用。

### 29. pg_statement_rollback — 保留

- 原名：`pg_statement_rollback-1.6-pg19-compat.patch`。
- 当前/归档名称：`pg_statement_rollback-1.6-pg19-compat.patch`。
- 必要性：PG19 post-parse hook 使用 const JumbleState。
- 最小性：同一条件宏覆盖 callback 声明和定义。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pg_statement_rollback-1.6-pg19-compat.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pg_statement_rollback/patches/pg_statement_rollback-1.6-pg19-compat.patch)。
- rpm PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/packaging03-fix/rpm/pg_statement_rollback.json)。
- deb PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/statement-order/deb/pg_statement_rollback.json)。

### 30. pg_stl — 保留

- 原名：`pg_stl-1.0.0-pg19-compat.patch`。
- 当前/归档名称：`pg_stl-1.0.0-pg19-tuple-header.patch`。
- 必要性：元组声明不再间接引入。
- 最小性：单一 include。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pg_stl-1.0.0-pg19-tuple-header.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pg_stl/patches/pg_stl-1.0.0-pg19-tuple-header.patch)。
- rpm PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01/rpm/pg_stl.json)。
- deb PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers01-deb/deb/pg_stl.json)。

### 31. pg_textsearch — 保留

- 原名：`pg_textsearch-1.5.1-pg19-compat.patch`。
- 当前/归档名称：`pg_textsearch-1.5.1-pg19-limits-header.patch`。
- 必要性：limits 声明不再间接引入。
- 最小性：单一 limits.h include。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pg_textsearch-1.5.1-pg19-limits-header.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pg_textsearch/patches/pg_textsearch-1.5.1-pg19-limits-header.patch)。
- rpm PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/compat03/rpm/pg_textsearch.json)。
- deb PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/compat03/deb/pg_textsearch.json)。

### 32. pg_uint128 — 上游已替代，本批不提交

- 原名：`pg_uint128-1.2.0-arithmetic-commutators.patch`。
- 当前/归档名称：`pg_uint128-1.2.0-arithmetic-commutators.patch`。
- 必要性：旧 1.2.0 算术 commutator 问题已由 1.3.0 上游替代。
- 最小性：不再被配方引用，不作为本批适用补丁提交；保留用户原文件，不为旧版本扩大审查。
- 充分性与边界：仅确认已被上游替代且无引用；未逐行复核不再应用的大型 SQL 补丁。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pg_uint128-1.2.0-arithmetic-commutators.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pg_uint128/patches/pg_uint128-1.2.0-arithmetic-commutators.patch)。
- rpm PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/upgrade02-fix2/rpm/pg_uint128.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-compat-rpm-19.json)。
- deb PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/upgrade02-fix2/deb/pg_uint128.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-compat-deb-19.json)。

### 33. pg_uint128 — 上游已替代，本批不提交

- 原名：`pg_uint128-1.2.0-comparison-commutators.patch`。
- 当前/归档名称：`pg_uint128-1.2.0-comparison-commutators.patch`。
- 必要性：旧 1.2.0 比较 commutator 问题已由 1.3.0 上游替代。
- 最小性：不再被配方引用，不作为本批适用补丁提交；保留用户原文件，不为旧版本扩大审查。
- 充分性与边界：仅确认已被上游替代且无引用；未逐行复核不再应用的大型 SQL 补丁。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pg_uint128-1.2.0-comparison-commutators.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pg_uint128/patches/pg_uint128-1.2.0-comparison-commutators.patch)。
- rpm PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/upgrade02-fix2/rpm/pg_uint128.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-compat-rpm-19.json)。
- deb PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/upgrade02-fix2/deb/pg_uint128.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-compat-deb-19.json)。

### 34. pg_uint128 — 保留

- 原名：`pg_uint128-1.3.0-pg19-compat.patch`。
- 当前/归档名称：`pg_uint128-1.3.0-pg19-compat.patch`。
- 必要性：PG19 移除 signed int8 Datum 转换宏。
- 最小性：恢复有符号八位值的转换，覆盖 PG_RETURN_INT8 与 series；未使用 signedness 随架构变化的 CharGetDatum。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pg_uint128-1.3.0-pg19-compat.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pg_uint128/patches/pg_uint128-1.3.0-pg19-compat.patch)。
- rpm PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/upgrade02-fix2/rpm/pg_uint128.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-compat-rpm-19.json)。
- deb PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/upgrade02-fix2/deb/pg_uint128.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-compat-deb-19.json)。

### 35. pg_variables — 保留

- 原名：`pg_variables-1.2.5-attver.patch`。
- 当前/归档名称：`pg_variables-1.2.5-composite-datum.patch`。
- 必要性：手写 composite datum 复制遗漏版本信息。
- 最小性：用 core heap_copy_tuple_as_datum 代替手写 header/TOAST 路径；保持 PG15–18 安全小版本下限。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pg_variables-1.2.5-composite-datum.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pg_variables/patches/pg_variables-1.2.5-composite-datum.patch)。
- rpm PG19：`regression-failed`；PG19 配方未启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api08-followup/rpm/pg_variables.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api08-rpm-19.json)。
- deb PG19：`regression-failed`；PG19 配方未启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api08-followup/deb/pg_variables.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api08-deb-19.json)。
- deb PG18：`passed`；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-pg_variables-pg18.json)。
- rpm PG18：`passed`；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-pg_variables-pg18.json)。

### 36. pg_variables — 撤出并暂缓

- 原名：`pg_variables-1.2.5-pg19-compat.patch`。
- 候选已退出正式应用链，归档名称：`pg_variables-1.2.5-pg19-compat.patch`。
- 归档文件：[rpm](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/deferred-patches/rpm/rpmbuild/SPECS/patches/pg_variables-1.2.5-pg19-compat.patch) · [deb](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/deferred-patches/deb/debbuild/pg_variables/debian/patches/pg_variables-1.2.5-pg19-compat.patch)。
- 必要性：PG19 类型断言宏和 bits8 移除。
- 最小性：编译候选不足以解决 composite-record 回归失败，撤出应用链，保留安全修复而不放宽数据库检查。
- 充分性与边界：PG19 继续禁用；PG18 撤出候选后的构建/验包通过，不覆盖此前已记录的功能问题。
- rpm PG19：`regression-failed`；PG19 配方未启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api08-followup/rpm/pg_variables.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api08-rpm-19.json)。
- deb PG19：`regression-failed`；PG19 配方未启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api08-followup/deb/pg_variables.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api08-deb-19.json)。
- deb PG18：`passed`；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-pg_variables-pg18.json)。
- rpm PG18：`passed`；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-pg_variables-pg18.json)。

### 37. pgclone — 保留

- 原名：`pgclone-4.9.0-pg19-lsyscache.patch`。
- 当前/归档名称：`pgclone-4.9.0-pg19-lsyscache.patch`。
- 必要性：数据库查名声明改由 lsyscache.h 提供。
- 最小性：在三个实际调用单元显式 include。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pgclone-4.9.0-pg19-lsyscache.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pgclone/patches/pgclone-4.9.0-pg19-lsyscache.patch)。
- rpm PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/upgrade01-fix/rpm/pgclone.json)。
- deb PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/upgrade01-fix/deb/pgclone.json)。

### 38. pgnodemx — 保留

- 原名：`pgnodemx-2.0.1-pg19-compat.patch`。
- 当前/归档名称：`pgnodemx-2.0.1-pg19-tuplestore.patch`。
- 必要性：tuplestore 声明不再间接引入。
- 最小性：单一 include。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pgnodemx-2.0.1-pg19-tuplestore.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pgnodemx/patches/pgnodemx-2.0.1-pg19-tuplestore.patch)。
- rpm PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers02/rpm/pgnodemx.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-pgnodemx-rpm-19.json)。
- deb PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers02/deb/pgnodemx.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-functional-deb-19.json)。

### 39. pgpdf — 保留

- 原名：`pgpdf-0.1.0-pg19-compat.patch`。
- 当前/归档名称：`pgpdf-0.1.0-pg19-datum-pointers.patch`。
- 必要性：varlena accessor 需要真实指针。
- 最小性：两处 DatumGetPointer，保持长度和复制字节。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pgpdf-0.1.0-pg19-datum-pointers.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pgpdf/patches/pgpdf-0.1.0-pg19-datum-pointers.patch)。
- rpm PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/compat03/rpm/pgpdf.json)。
- deb PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/compat03/deb/pgpdf.json)。

### 40. pgspider_ext — 保留

- 原名：`pgspider_ext-1.3.0-pg19-compat.patch`。
- 当前/归档名称：`pgspider_ext-1.3.0-pg19-compat.patch`。
- 必要性：PG19 slot 初始化新增 flags，相关声明不再间接引入。
- 最小性：两个调用均传默认 0 flags；只补 hsearch 与 tuple 头文件。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pgspider_ext-1.3.0-pg19-compat.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pgspider_ext/debian/patches/pgspider_ext-1.3.0-pg19-compat.patch)。
- rpm PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api07/rpm/pgspider_ext.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api08-rpm-19.json)。
- deb PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api07/deb/pgspider_ext.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api08-deb-19.json)。

### 41. pgxicor — 保留

- 原名：`pgxicor-0.1.1-pg19-compat.patch`。
- 当前/归档名称：`pgxicor-0.1.1-pg19-compat.patch`。
- 必要性：limits、type、tuple 声明不再间接引入。
- 最小性：只补实际使用的三个头文件。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pgxicor-0.1.1-pg19-compat.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pgxicor/patches/pgxicor-0.1.1-pg19-compat.patch)。
- rpm PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers02/rpm/pgxicor.json)。
- deb PG19：`smoke-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/headers02/deb/pgxicor.json)。

### 42. pldebugger — 保留

- 原名：`pldebugger-1.10-pg19-compat.patch`。
- 当前/归档名称：`pldebugger-1.10-pg19-compat.patch`。
- 必要性：PG19 lock tranche 直接接收名称，shared hash 改为固定容量。
- 最小性：仅调整 tranche 注册方式与两个 hash 调用；旧版保留原签名。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pldebugger-1.10-pg19-compat.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/pldebugger/debian/patches/pldebugger-1.10-pg19-compat.patch)。
- rpm PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api07/rpm/pldebugger.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api08-rpm-19.json)。
- deb PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api07/deb/pldebugger.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api08-deb-19.json)。

### 43. plphp — 保留

- 原名：`plphp-2.6-pg19-compat.patch`。
- 当前/归档名称：`plphp-2.6-pg19-tuplestore.patch`。
- 必要性：两个 PL/PHP 编译单元缺少 tuplestore 声明。
- 最小性：两个 include。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/plphp-2.6-pg19-tuplestore.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/plphp/debian/patches/plphp-2.6-pg19-tuplestore.patch)。
- rpm PG19：`build-failed`；PG19 配方未启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api08-followup/rpm/plphp.json)。
- deb PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api08-followup/deb/plphp.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-final-functions-deb-19.json)。

### 44. pointcloud — 保留

- 原名：`pointcloud-1.2.5-pg19-compat.patch`。
- 当前/归档名称：`pointcloud-1.2.5-pg19-compat.patch`。
- 必要性：bits8 移除，FuncnameGetCandidates 新增参数。
- 最小性：同宽 uint8 替代；PG19 分支传默认 NULL，保持旧版调用。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/pointcloud-1.2.5-pg19-compat.patch)。
- rpm PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api04/rpm/pointcloud.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-pointcloud-rpm-19.json)。
- deb PG19：`no-local-recipe`；PG19 配方未启用。

### 45. psql_bm25s — 保留

- 原名：`psql_bm25s-0.4.14-pg19-compat.patch`。
- 当前/归档名称：`psql_bm25s-0.4.14-pg19-compat.patch`。
- 必要性：PG19 table scan/index fetch API 新增 flags。
- 最小性：仅在 PG19 传入默认 0 flags。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/psql_bm25s-0.4.14-pg19-compat.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/psql_bm25s/debian/patches/psql_bm25s-0.4.14-pg19-compat.patch)。
- rpm PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api08-followup/rpm/psql_bm25s.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api08-rpm-19.json)。
- deb PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api08-followup/deb/psql_bm25s.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api08-deb-19.json)。

### 46. repmgr — 保留

- 原名：`repmgr-5.5.1-pg19-compat.patch`。
- 当前/归档名称：`repmgr-5.5.1-pg19-c11.patch`。
- 必要性：GNU89 不满足 PG19 头文件语言要求。
- 最小性：仅更换为 GNU11。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/repmgr-5.5.1-pg19-c11.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/repmgr/patches/repmgr-5.5.1-pg19-c11.patch)。
- rpm PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/static19-fix/rpm/repmgr.json)。
- deb PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/repmgr-deb-fix/deb/repmgr.json)。

### 47. rum — 保留

- 原名：`rum-1.3.15-pg19-compat.patch`。
- 当前/归档名称：`rum-1.3.15-pg19-compat.patch`。
- 必要性：Pointer 改为 void*，编码游标不能继续作隐式字节算术；相关 PG19 API 改动。
- 最小性：编码游标显式使用 char*，同步必要 Item/int8/varlena 调用；保持编码格式。补丁较长但各调用点均属同一类型边界。
- 充分性与边界：沿用已复核的 34/35 SQL 回归差异，以及通过的 isolation/TAP；不能标记全部 SQL 通过。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/rum-1.3.15-pg19-compat.patch)。
- rpm PG19：`partial-regression-reviewed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/rum-final/rpm/rum.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-rum-tail-rpm-19.json)。
- deb PG19：`no-local-recipe`；PG19 配方未启用。

### 48. sqlite_fdw — 保留

- 原名：`sqlite_fdw-2.5.0-pg19-compat.patch`。
- 当前/归档名称：`sqlite_fdw-2.5.0-pg19-compat.patch`。
- 必要性：PG19 instrumentation 类型、varlena 和声明变化。
- 最小性：只补声明、默认类型分支、Datum 转换和上游版本门禁。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/sqlite_fdw-2.5.0-pg19-compat.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/sqlite_fdw/debian/patches/sqlite_fdw-2.5.0-pg19-compat.patch)。
- rpm PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api08-final/rpm/sqlite_fdw.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-sqlite-rpm-19.json)。
- deb PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api08-final/deb/sqlite_fdw.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-sqlite-deb-19.json)。

### 49. temporal_tables — 保留

- 原名：`temporal_tables-1.2.2-pg19-compat.patch`。
- 当前/归档名称：`temporal_tables-1.2.2-pg19-hash-allocator.patch`。
- 必要性：PG19 hash allocator callback 新增 context 参数。
- 最小性：声明与定义同步；原 allocator 使用 TopMemoryContext，无需使用新增上下文。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/temporal_tables-1.2.2-pg19-hash-allocator.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/temporal_tables/patches/temporal_tables-1.2.2-pg19-hash-allocator.patch)。
- rpm PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api04/rpm/temporal_tables.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api04-rpm-19.json)。
- deb PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api04/deb/temporal_tables.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api04-deb-19.json)。

### 50. ulak — 修正后保留

- 原名：`ulak-0.3.0-compat.patch`。
- 当前/归档名称：`ulak-0.3.0-hiredis-keepalive.patch`。
- 必要性：EL9 hiredis 1.0 没有 interval-aware keepalive API。
- 最小性：保留必要的 hiredis 版本条件；移除目标平台不再需要的 libcurl <7.66 分支，缩为单文件补丁。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/ulak-0.3.0-hiredis-keepalive.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/ulak/patches/ulak-0.3.0-hiredis-keepalive.patch)。
- rpm PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/upgrade02-fix/rpm/ulak.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-functional-rpm-19.json)。
- deb PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/batch08/deb/ulak.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-functional-deb-19.json)。
- deb PG19：`passed`；PG19 配方未启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-ulak-pg19.json)。
- rpm PG19：`passed`；PG19 配方未启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-ulak-pg19.json)。

### 51. ulak — 保留

- 原名：`ulak-0.3.0-pg19-compat.patch`。
- 当前/归档名称：`ulak-0.3.0-pg19-compat.patch`。
- 必要性：PG19 numeric_int4_safe 使用 ErrorSaveContext。
- 最小性：保留非抛错 overflow 检测与原 retry 上限处理，不能用 NULL 直接替代。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/ulak-0.3.0-pg19-compat.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/ulak/patches/ulak-0.3.0-pg19-compat.patch)。
- rpm PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/upgrade02-fix/rpm/ulak.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-functional-rpm-19.json)。
- deb PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/batch08/deb/ulak.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-functional-deb-19.json)。
- deb PG19：`passed`；PG19 配方未启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/deb-ulak-pg19.json)。
- rpm PG19：`passed`；PG19 配方未启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/review-commits/builds/rpm-ulak-pg19.json)。

### 52. vasco — 保留

- 原名：`vasco-0.1.0-pg19-compat.patch`。
- 当前/归档名称：`vasco-0.1.0-pg19-tuple-header.patch`。
- 必要性：元组声明不再间接引入。
- 最小性：单一 include。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/vasco-0.1.0-pg19-tuple-header.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/vasco/patches/vasco-0.1.0-pg19-tuple-header.patch)。
- rpm PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/compat03/rpm/vasco.json)。
- deb PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/compat03/deb/vasco.json)。

### 53. vgram — 保留

- 原名：`vgram-1.0-pg19-compat.patch`。
- 当前/归档名称：`vgram-1.0-pg19-compat.patch`。
- 必要性：Pointer 改为 void* 且 varlena 参数收紧。
- 最小性：编码指针明确使用 char*，两处 DatumGetPointer；保持字节偏移语义。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/vgram-1.0-pg19-compat.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/vgram/debian/patches/vgram-1.0-pg19-compat.patch)。
- rpm PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api07-followup/rpm/vgram.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api08-rpm-19.json)。
- deb PG19：`regression-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api07-followup/deb/vgram.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api08-deb-19.json)。

### 54. wal2mongo — 保留

- 原名：`wal2mongo-1.0.7-pg19-compat.patch`。
- 当前/归档名称：`wal2mongo-1.0.7-pg19-compat.patch`。
- 必要性：PG19 replication-origin 命名、类型断言和 varlena API 变化。
- 最小性：局部版本别名、保留 static 检查、显式 Datum 转换。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/wal2mongo-1.0.7-pg19-compat.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/wal2mongo/debian/patches/wal2mongo-1.0.7-pg19-compat.patch)。
- rpm PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api08/rpm/wal2mongo.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api08-rpm-19.json)。
- deb PG19：`functional-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api08/deb/wal2mongo.json)；[运行证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/runtime/regression-api08-deb-19.json)。

### 55. zhparser — 保留

- 原名：`zhparser-2.3-pg19-compat.patch`。
- 当前/归档名称：`zhparser-2.3-pg19-lsyscache.patch`。
- 必要性：get_namespace_oid 的声明位置变化。
- 最小性：单一 lsyscache.h include；保留 CRLF 补丁字节及 --binary 应用方式。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[rpm](/Users/vonng/pgsty/rpm/rpmbuild/SPECS/patches/zhparser-2.3-pg19-lsyscache.patch) · [deb](/Users/vonng/pgsty/deb/debbuild/zhparser/patches/zhparser-2.3-pg19-lsyscache.patch)。
- rpm PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/zhparser-final/rpm/zhparser.json)。
- deb PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/zhparser-final/deb/zhparser.json)。

### 56. repmgr — 保留

- 原名：`target-server-headers.patch`。
- 当前/归档名称：`target-server-headers.patch`。
- 必要性：DEB libpq internal 头文件可能属于另一 PG 主版本。
- 最小性：仅将目标 server include 路径提前；Debian quilt 中采用目的明确的原生补丁名。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[deb](/Users/vonng/pgsty/deb/debbuild/repmgr/patches/target-server-headers.patch)。
- rpm PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/static19-fix/rpm/repmgr.json)。
- deb PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/repmgr-deb-fix/deb/repmgr.json)。

### 57. hdfs_fdw — 保留

- 原名：`hdfs_fdw-2.3.3-pg19-compat.patch`。
- 当前/归档名称：`hdfs_fdw-2.3.3-pg19-version-check.patch`。
- 必要性：HDFS FDW 上游构建列表没有 PG19。
- 最小性：仅扩充已构建验证的版本门禁。
- 充分性与边界：已有构建、payload 与回归证据的覆盖范围见证据；未将编译成功等同于完整功能验收。
- 文件：[deb](/Users/vonng/pgsty/deb/debbuild/hdfs_fdw/debian/patches/hdfs_fdw-2.3.3-pg19-version-check.patch)。
- rpm PG19：`no-local-recipe`；PG19 配方未启用。
- deb PG19：`payload-passed`；PG19 配方启用；[构建证据](/Users/vonng/pgsty/artifacts/nonrust-pg19-20261121/results/api07/deb/hdfs_fdw.json)。

## 按扩展拆分的提交

下表按源码构建单元归并两仓库提交；一个源码产生多个子包时保持同一语义提交。各扩展的共享 Makefile target 修改已随本扩展提交，公共构建策略另列。

| 扩展 / 组件 | RPM commit | DEB commit |
|---|---|---|
| acdat | `820331ea8b15` | `c87da1ccea65` |
| address_standardizer | `5e63c45a40a6` | `249a0a052f5b` |
| addressing_dictionary | `4807a103798e` | `737eb86a1e73` |
| aggs_for_arrays | `882387373dd9` | `878de2a6ab39` |
| aggs_for_vecs | `2c8bc7993cdd` | `6d647e4bfb4e` |
| argm | `894083c90ce1` | `495bef347680` |
| asn1oid | `5fe34040f424` | — |
| aws_s3 | `20e5d9525d66` | `a8bb48056ec9` |
| cat_tools | `4debfa175607` | `1ba3ad0d39a0` |
| cgal54 | `7c43016a9924` | — |
| chkpass | `49b0ead8c8e5` | `1d9a96f96dd1` |
| codesystem | `b510e98f54c2` | — |
| colnames | `0ba4adfa540b` | `6b68b0d2b44d` |
| column_encrypt | `2434386d39b5` | `ed4d72e758a3` |
| count_distinct | `e13f6ae067bc` | `859e4960bea3` |
| credcheck | `047825a449bc` | — |
| cron_utils | `e22c236c37f1` | `fe0854d47026` |
| cryptint | `d54fa10f2378` | `e1e2be66bdfc` |
| data_historization | `a84f881a65b3` | `0b3de4c1f69b` |
| datasketches | `1dda884aaef4` | `ae648f8e494d` |
| db2fce | `eb046994301d` | — |
| db_migrator | `0c4cbdd3de19` | `c5d71c8404d3` |
| dbt2 | `28f30960b863` | `4aa9a3689369` |
| ddl_historization | `34142faea73d` | `e4bd01f5222f` |
| ddsketch | `099aa6858139` | `b8a1045d8018` |
| decoder_raw | `ab05e5806a79` | `5430fc9ce346` |
| decoderbufs | `4d15922a5f19` | `1bc632be90a9` |
| documentdb | `6d8f4f954bf0` | `e1ebc84519d5` |
| emaj | `6882e1b9c985` | `3228dd469083` |
| external_file | `73db7095788e` | `414414b7a8df` |
| faker | — | `931dee93be45` |
| fbsql | `0227b2355461` | `635db2efa192` |
| firebird_fdw | `10a68fd4ff2c` | `b6b6ad32de90` |
| first_last_agg | `817050164804` | — |
| floatfile | `f3eda32b3715` | `8f5b444a02a3` |
| floatvec | `0673457966e2` | `0b132456c2cc` |
| fsm_core | `ca40a6ecedc7` | `62c6208364d9` |
| gdal38 | `985b185f5c39` | — |
| geoip | `5ab893669d32` | `a998631c4318` |
| graphblas | `5f0ad7a87917` | `f7a767a3ce42` |
| h3-pg | `30e196514cec` | `49ac83e8b711` |
| haproxy | `e54533423446` | `921a80ad7369` |
| hashtypes | `366a1c266c14` | `74f846a459a3` |
| hdfs_fdw | — | `c9e60348855a` |
| hdr_histogram | `dd06e2363b08` | `6354671cc904` |
| hunspell | `e90a080c4199` | `dcb63eede1d1` |
| icu_ext | `18f42213c120` | — |
| imgsmlr | `901ccbd9e48e` | `f3fb48017fa6` |
| index_advisor | `9a99e13d5c2e` | `9611b3a253ac` |
| is_jsonb_valid | `38febd379a4c` | `ae955885ffa4` |
| istore | `4123cfad6d12` | `b4c9b3018fdb` |
| jdbc_fdw | `d294a0d2c001` | `13b65370da1d` |
| jev | `8e753d404f1e` | `8712f4a8af9d` |
| kafka_fdw | `2019aa053718` | `0aac85c884fa` |
| lagraph | `5737b50c7fb9` | `3eb9e6638eda` |
| libpgfeutils15 | `91e46e5fd164` | — |
| libpgfeutils16 | `65d9b998f27e` | — |
| libpgfeutils17 | `228af84e570b` | — |
| libpgfeutils18 | `647c594bb3b5` | — |
| libx509pq | `aa0a94bf8350` | `33c048a11b97` |
| log_fdw | `135b653374b2` | `4f654ccceed9` |
| logerrors | — | `407419499523` |
| logical_ddl | `d03c5f64218d` | `b240cb530981` |
| login_hook | `a2c98ab2d841` | `2ed1bc818ec9` |
| lower_quantile | `ae0e755f1e79` | `603e8f3d0b26` |
| macavity | `5f3aa31464c2` | `c37b08134ceb` |
| md5hash | `a8acba3a09c0` | `f44955b371a7` |
| mimeo | `78621cf80243` | — |
| mobilitydb | `d83b96d3fc28` | `fdcd4b48a511` |
| mongo_fdw | `1b797550aa70` | `3e5619b2f387` |
| multicorn | — | `a3b83d484b14` |
| mysqlcompat | — | `3335c4ba81c3` |
| nominatim_fdw | `40b9166fa37a` | `c329d1e5f43b` |
| numeral | `775a55b1c5e0` | — |
| oai_fdw | `352fb7a777e6` | `962bcecda49f` |
| odbc_fdw | — | `2656ef06d879` |
| omnisketch | `e23b94378aab` | `dce7fccbc850` |
| onesparse | `1981b9bc019e` | `00285120c8de` |
| online_advisor | `3bfd81625156` | `071569d0683a` |
| pagevis | `85408ecef36c` | `9d72df1a14e9` |
| parray_gin | `d840dbe6d38b` | `008712f945c3` |
| passwordcheck_cracklib | `bf6f1aa099e7` | `06597a3017d7` |
| passwordpolicy | `fc317838a696` | `4876a06868d4` |
| pdu | `2f5528bbc867` | `63da787e6149` |
| periods | `3f96d9bb79e0` | — |
| permuteseq | `467a29443006` | `9aba1df957d2` |
| pg4ml | `0e7e937cf9d0` | `fa56778d1441` |
| pg_accumulator | `9509141cd3c7` | `4aebdc512c7f` |
| pg_acl | `eb3306db234e` | `abf8cae18af1` |
| pg_adhoc | `dde320d96d98` | — |
| pg_ai_query | `b9005bcfcb1e` | `f5e4cc74452d` |
| pg_arraymath | `f41f2b4108bd` | `4053b88765f5` |
| pg_ash | `5a106a964a0a` | `0072b92a50fc` |
| pg_auditor | `09308e6c126f` | `ab8b2415784e` |
| pg_auth_mon | `642532b1a4ff` | `1a4e03017932` |
| pg_background | `066cad3e007a` | `b0d6c22eaf84` |
| pg_base36 | `b847dbe4399a` | `e8842f102237` |
| pg_base62 | `2896d6973b1a` | `922de8830807` |
| pg_bigm | `c9c9d5406c9a` | `5329b0801fc1` |
| pg_bikram_sambat | `464e8566bf97` | `52fd4ee92a3d` |
| pg_biscuit | `a98225d3f34b` | `db390ee46243` |
| pg_bulkload | `3309bc06da16` | `f7c657ded2b6` |
| pg_byteamagic | `fd38701ca013` | `898502c00547` |
| pg_bzip | `98c6de3c8ad1` | `1bdca5076892` |
| pg_cheat_funcs | `bdc72a015c43` | `82c66895d194` |
| pg_checksums | `734021325da7` | `4ef906de808c` |
| pg_cjk_parser | `1f1141651c26` | `2fc98e784387` |
| pg_clickhouse | `ff5b821fddcd` | `d02dafc3494e` |
| pg_column_tetris | `61b08f622c5d` | `d44f0e250515` |
| pg_cooldown | `2e483f7b9fb6` | `888850af9506` |
| pg_country | `078abaac1f44` | `33cbcde6ca49` |
| pg_crash | `a93f955c7681` | `112073473522` |
| pg_csv | `37a818b190f0` | — |
| pg_curl | `f8839613b715` | `f7a6aba35a30` |
| pg_currency | `4c1d9ec4841e` | `22c0609f1286` |
| pg_datasentinel | `bc01f5f204ca` | `f660d021415a` |
| pg_dbms_errlog | — | `151d21caa618` |
| pg_dbms_job | — | `cd5fcef6fb01` |
| pg_dbms_lock | — | `eef3320dccb5` |
| pg_dbms_metadata | `c841b7ec96e1` | `55c272d73df8` |
| pg_ddlx | `70634e8826e2` | `2757faac65fe` |
| pg_describe | `07f89aa65f1b` | `9f871853288f` |
| pg_dirtyread | `93dd03a4eea7` | — |
| pg_disorder | `339d2c4e5907` | `dafe6b3c021f` |
| pg_dispatch | — | `971760cc04db` |
| pg_drop_events | `ca5407b7a1ec` | `5a86cac192c1` |
| pg_duration | `abc550338342` | `c6bd7805df87` |
| pg_ecdsa | `203349d89157` | `97be7688f61a` |
| pg_emailaddr | `6ac34d49e824` | `961868cdfce2` |
| pg_envvar | `60420e09e40d` | `ee69be5a74d4` |
| pg_extra_time | `ff2ac97ca900` | `53ee3f4f369c` |
| pg_fact_loader | — | `89583f32dcf2` |
| pg_failover_slots | `cbe15eaa88cb` | `52279b4dd747` |
| pg_financial | `82435d5d1cbf` | `174636845213` |
| pg_fio | `57609bf959b9` | `74119a57ce29` |
| pg_fkpart | — | `187834c4eb4f` |
| pg_flight_recorder | `76e024a665dc` | `9e0f004472f4` |
| pg_fsql | `385316458a7b` | `f89dfcdfa32e` |
| pg_fts | `9c9a1ba06207` | `77fa214b2fed` |
| pg_geohash | `735e86a45e6d` | `12ceeeca91d2` |
| pg_grammar_guard | `3d47ff56e497` | `0cdc9fd71a1a` |
| pg_gzip | `ce70b7cd764d` | `c30467b44938` |
| pg_hashids | `633bcecacc5a` | `b7aada22c7b5` |
| pg_hashlib | `b8c945cd3df2` | `1995687187ab` |
| pg_html5_email_address | `7c1d73960651` | `5670f40bac76` |
| pg_http | `bee6a6d584d6` | `a300d650f8c8` |
| pg_icu_parser | `617a20e10f61` | `b3ffb3e07fb0` |
| pg_incremental | `a64c1ad7d956` | `1be5aa4d4d7d` |
| pg_integrity_checksums | `0dfb37c9bd0d` | `463840bb7f19` |
| pg_isok | `465c40132b03` | `7c4b001c0f92` |
| pg_ivm | `4546a338d7c4` | `3ea274c41411` |
| pg_jieba | `8e277b211c23` | `067774ca7941` |
| pg_jobmon | — | `1bc4ef08bd09` |
| pg_json_diff | `64e3b3e79e3e` | `0049c409f648` |
| pg_kpart | `4b690f95b0d7` | `6ad68e6d9451` |
| pg_lease | `c4a4f4cc9d9c` | — |
| pg_lion | `b70b31fdf535` | `c42f99071093` |
| pg_liquid | `859f8c3bf8be` | `239409f83482` |
| pg_living_assertions | `80582fa32a0f` | `dde677ad92ec` |
| pg_local_cache | `14ca899554cd` | `83eba883b3c3` |
| pg_math | `c5c65f042c30` | `653800914d0e` |
| pg_meta | `e6db78562f75` | `d46c9d3a5023` |
| pg_mockable | `c8f2e9eb7702` | `6cb2b6fed1e2` |
| pg_mon | — | `1c13ae79d79f` |
| pg_nanotime | `a4ea2b6426b4` | `c152c75a9e0f` |
| pg_net | `a0f800d11cf7` | `9a36f999f896` |
| pg_noset | `7a5cfd8200e4` | `fc9d17d961d2` |
| pg_oidc_validator | — | `b4da8b28181b` |
| pg_opencc | `64157fc2c0ef` | `d15b51de4a00` |
| pg_orphaned | `c95e3a37ca3f` | `76c5cc2af94f` |
| pg_partman | `abe81ec6430a` | `a22765482e6c` |
| pg_permissions | `bad33928f195` | `959555645435` |
| pg_plan_filter | `3feb5bc074c6` | `edd2a0b6d889` |
| pg_policy | `928ae14f3ef9` | `37a7a944e3f4` |
| pg_prefix | `bf0a6730f93e` | — |
| pg_profile | `42885a413f00` | `633247db6d07` |
| pg_projection | `fef3eae336d3` | `8f5194cbb5f0` |
| pg_protobuf | `bdd1ae978893` | `119562deae5b` |
| pg_qos | `379405741f72` | `3e79247c87f1` |
| pg_query_rewrite | `16b7c6a9b6c5` | `a830aee215c7` |
| pg_random | `b7489d76187a` | `b333251d039f` |
| pg_rational | `ab6b02dd1acb` | — |
| pg_readme | `371bf1d727db` | `951dcc124536` |
| pg_readonly | `ed5ffbb7da13` | `477c211474c6` |
| pg_redis_pubsub | `814f106d39ef` | `eeaa6ae0606c` |
| pg_regresql | `f0cc7299d071` | `1d2174caa698` |
| pg_relation_sql | `17a83c14205d` | `f99f058acfa0` |
| pg_relusage | `4fb323e286ea` | `a0448286e3c7` |
| pg_retry | `3403c78c95d3` | `b315f9aa42c1` |
| pg_rewrite | `5416a5806a62` | `b81107a70a55` |
| pg_roaringbitmap | `c4e1439c5934` | `f9ff8a8af141` |
| pg_roast | `a3f9acfc07c5` | `1407e867d287` |
| pg_rrule | `b7f8a1134a6e` | — |
| pg_rusage | `3f1fdd7501be` | `3d02388cbb30` |
| pg_savior | `87a732630daf` | `a5ff47f8aa03` |
| pg_schedoc | `f980e3a08238` | `11ee4f3acb66` |
| pg_semver | `76072f6d891a` | `0e69fdb5c37d` |
| pg_similarity | `8609c523d7c9` | — |
| pg_slug_gen | `c4d88a82760f` | `03f348ca37bc` |
| pg_snakeoil | `138a5231c1ac` | — |
| pg_sorted_heap | `73ba8277824a` | — |
| pg_sqlog | `045760d35809` | `e46f43b621be` |
| pg_stat_backtrace | `7a9fc7629e06` | `53acbb363a26` |
| pg_stat_monitor | `73d4ea369991` | `9d6743a35f18` |
| pg_stat_plans | `d72d10faafa9` | `a0e7ba4630aa` |
| pg_stat_tcpinfo | `6c3223abdcb7` | `1ee1a4d0cd91` |
| pg_statecharts | `6bb6f151d0d3` | `2efc2e96ce7f` |
| pg_statement_rollback | `c1681d3726e0` | `be4dea27089d` |
| pg_statvfs | `2abbfdc7dbe4` | `1c56517ad414` |
| pg_statviz | `e6c5b3a947e0` | `8b7d93e5c672` |
| pg_stl | `fd166e8a9241` | `2fb71eff2ec2` |
| pg_store_plans | `11ed4d24e6e1` | `df2895742ab2` |
| pg_strom | `5156b0cb00a6` | — |
| pg_synonym | `d04a0d87697e` | `850af51478c5` |
| pg_task | `944129c1c2a5` | `5b22e7d54a37` |
| pg_text_semver | `cb35178406ab` | `b906aa344fcb` |
| pg_textsearch | `251e3a2b4f2f` | `e3c721ffb0fc` |
| pg_tiktoken_c | `82d3e2a64f74` | `039bfbe4bcae` |
| pg_timeit | — | `aad46512baf5` |
| pg_timeseries | `a1085e05f580` | `7b7aedaa01d1` |
| pg_tle | `6e3d04c54c3a` | `978432bfbf7d` |
| pg_tracing | `87ff46bcef46` | `3aeeca75fe7c` |
| pg_track_optimizer | `c9ca768cae6f` | — |
| pg_tre | `d6ce1bf8c233` | `a773435840c2` |
| pg_try_cast | `746fb91b42fd` | `e4ed866b4520` |
| pg_ttl_index | `23260f38e207` | `945cc9214a36` |
| pg_uint128 | `48d509dd5dee` | `42c0cdc5eaf4` |
| pg_upless | `501d8810ccfb` | `0ea80f44cbda` |
| pg_uri | `0410aa24e1fb` | `5dc9d748d875` |
| pg_utl_smtp | `2234609bea47` | `12d12841f5da` |
| pg_uuid_v8 | `997968695e8d` | `494bd7481825` |
| pg_uuidv7 | — | `33d4ae892fa7` |
| pg_variables | `2a643f5621c4` | `c5d59e449c3e` |
| pg_vault | `d00b91ce8bd2` | `bdae90288d54` |
| pg_vectorsearch | `bc7af41bdd18` | `84ba497e71a2` |
| pg_wait_sampling | `1fe68de9f217` | — |
| pg_weighted_statistics | `e264a93e23ec` | `d07df91b1e86` |
| pg_xenophile | `9a04f1d0d44c` | `fc1068b34c93` |
| pg_xxhash | `bc1acda06b44` | `8fae8978fb73` |
| pg_zstd | `4b0444e9176a` | `4612ac30ed28` |
| pgactive | `7dc3c7b3cb26` | `feaaed3aed38` |
| pgaudit | `cf45cc562cbb` | — |
| pgautofailover | `c25d3d853320` | — |
| pgbouncer_fdw | — | `a26e9f93cdb7` |
| pgcalendar | — | `844fb0655846` |
| pgclone | `47230d250165` | `178045714c82` |
| pgcollection | `1bcb2b01c43e` | `b68e6e18933c` |
| pgcopydb | `7c76905efeed` | — |
| pgcozy | `57da1111abc6` | `33d480d9b510` |
| pgcryptokey | `c79c522f5c9e` | `d9f38aa1b2a6` |
| pgdisablelogerror | — | `be58f2a018fc` |
| pgelog | — | `ce2c9cf4b7c8` |
| pgexporter_ext | `d383481e7b3d` | `165e85d94572` |
| pgextwlist | `d94bd3c7b024` | `26e5fefefcd9` |
| pgfaceting | `a00ad185909a` | — |
| pgfincore | `a2e100231dc8` | `5c6d6dc5229c` |
| pghydro | `a90873dcb0ed` | `453051e41b67` |
| pgjq | `1172256e9e9e` | `5396a7ee1030` |
| pgjwt | `4dc84c29fa0a` | `fdc2fdbecd69` |
| pgl_ddl_deploy | `a1c20babdd28` | `6ebb37cac920` |
| pglock | — | `3d5e0eda07bc` |
| pglogical_ticker | `d194791fbb1c` | `eeb8b23172ab` |
| pgmb | `20cd130678ad` | `82b51d27f722` |
| pgmemcache | `1dfbcbebc948` | — |
| pgmemento | `d74d13ee0861` | `0da6d74de5ff` |
| pgmeminfo | `5785b933d08a` | `ad68602e14ec` |
| pgmnemo | `36c1a19b713a` | `0b1e131c5741` |
| pgmonitor | `6434e47572c4` | `4cd714bf4b13` |
| pgmp | `756dd108e522` | `2ace1fd25382` |
| pgmq | `5bc8d65f9090` | `23030f580032` |
| pgnodemx | `c661c12e0323` | `6bab84e06294` |
| pgpcre | `513810139e0d` | — |
| pgpdf | `5eabb0ceead1` | `c6137c053b77` |
| pgproto | `c3eaf2ba4e59` | `9b6c8af20f5e` |
| pgq | `d5013536e9f9` | `d4d23462ad76` |
| pgqr | `8052c042e7e9` | `f0125dd8adfd` |
| pgroonga | `d59eec1f1eb4` | `025413c46384` |
| pgsentinel | `5b00a4a94fc5` | `68bce5ea1cdb` |
| pgsodium | `215be366e8e2` | `08b749453cc0` |
| pgsparql | `8b1e1d124ecc` | `d2e4f80a3671` |
| pgsphere | `5a409f683386` | — |
| pgspider_ext | `354f9fbe9b10` | `465358c3b800` |
| pgsql_tweaks | `5d975adca2ee` | `51c78351d558` |
| pgsqlmock | `c88fa30a1de8` | `39930bc183bc` |
| pgtelemetry | `f017ac359d0d` | `1a3e20bbe130` |
| pgtt | `1f6e38d53a5a` | `0b1d0be85726` |
| pguint | `309ada8e4c4f` | `40be9b147581` |
| pgunit | `506759b92aa2` | `0be1004be712` |
| pgvector | `35b82d9be53e` | `20bd41a66b48` |
| pgxicor | `10b3d8953e2c` | `2a068f6b7f46` |
| pgzint | — | `57328479a8e5` |
| pldebugger | `fc67b29145c2` | `f8cc12269c48` |
| pljs | `44915e58b7b2` | `2a51fbca3c81` |
| pllua | `a21c266b4640` | — |
| plpgsql_check | `ca41b077e8f2` | `83f490531e18` |
| plpgsql_wrap | — | `b8676f43d297` |
| plphp | `79a2afdabf7d` | `79169d1e8943` |
| plproxy | `639730f67aae` | `c92b16bf44dc` |
| plr | `5b1475adfa72` | `c5675b58cbca` |
| plruby | `77243586bec7` | `f0eefacf789e` |
| plx | `f0a581189870` | `20dba7ab7181` |
| plxslt | — | `86a2a26f8ac7` |
| pointcloud | `357eae085ade` | — |
| postbis | `5395dd225878` | `26154fae70f2` |
| postgis | `d9e29cf4a036` | `352b4b748ce7` |
| postgis_tiger_geocoder | `74d2b1a7440a` | `f858ce3a1260` |
| postgresbson | `b2ecbf437c8c` | `c7cfde0df3e0` |
| postgresql_anonymizer | — | `8a82f3e7a8bd` |
| powa | `0ec9515ec635` | `76fff36c21be` |
| preprepare | `a76e7b557df8` | — |
| proj96 | `59a695cf37f8` | — |
| provsql | `335e42e7ebb5` | `70aa8e7760c0` |
| psql_bm25s | `7f9c025fd034` | `0ada8b335ed0` |
| q3c | `9a6ac79e14f0` | `00d16085f8fd` |
| qdgc | `ded56e7ae8a3` | `dd0292903a5f` |
| quantile | `1900e0d06aea` | `10071f7a6993` |
| rdf_fdw | `a7e8745eb7a9` | `e9475961bf90` |
| rdkit | `d8c9aa189a05` | `ab58c321d5f5` |
| re2 | `5270aa9cbe8c` | `fcc141085e8f` |
| redis_fdw | `e1cd72c396fa` | `bdba35f1c62b` |
| repmgr | `c18f127600b1` | `9a7775ee6ff3` |
| rum | `de49384517cc` | — |
| safeupdate | `fc50fda4f634` | `f44bad12239d` |
| sequential_uuids | `19bc921e1845` | `87af5d92ba16` |
| session_variable | `30e2ea01b0d8` | `e5a105969420` |
| shacrypt | `19261703a7fe` | `bdd2fedb5492` |
| smlar | `987c8bfd7cc0` | `03132a22b672` |
| sqlite_fdw | `3ba9aecaa013` | `66bdf0341e38` |
| sslutils | `ed55284e6202` | `bc256a7a9a1a` |
| storage_engine | `b8d9f3fbe419` | `b7f1edc03e78` |
| supautils | `72fb3a55e06c` | `1d5d50ece9e7` |
| system_stats | `e3fba9ab3745` | `19d6cd763100` |
| table_log | `d76b32203e14` | — |
| table_version | `6419f0bbbf7f` | `5807408efeef` |
| temporal_tables | `18d437ae6f4b` | `7b50675adac8` |
| textsearch_intl | `c53a2f1778d1` | `cf03a5755071` |
| timescaledb | `0136012a6ca3` | `72b915292d68` |
| timestamp9 | `ce7b643a2636` | `c6bb853943ec` |
| toastinfo | `4bb17a8800a5` | — |
| topn | `47056f1f7d59` | `7d25c35f44e2` |
| ulak | `ceb49f7f310b` | `ad7d85afaff8` |
| url_encode | `542294fa1fa1` | `35866dffae13` |
| valkey | `191d0dbe96b1` | `cbe5d1619c89` |
| vasco | `29daf0c39bce` | `427c9c5f1fab` |
| vgram | `c52b47cfb80b` | `a0b22f805c6c` |
| wal2mongo | `9f2b328676b1` | `d2375a6dc085` |
| zhparser | `9ac275a13ec6` | `e7db894a33f4` |

公共编排提交：

- rpm `9d9e74d0ae17` — retire pg14 and el8 from default build orchestration。
- deb `45494114f7f9` — align default deb build targets with pg15-19。

完整 SHA、父提交与路径列表保留在 `unit-commits.jsonl`；已与 Git 实际提交链逐项核对，无重复单元或混入的其他扩展路径。
