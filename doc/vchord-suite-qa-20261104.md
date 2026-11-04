# vchord / vchord_bm25 / pg_tokenizer 独立验收：2026-11-04

## 结论

本批 `vchord 1.2.0`、`vchord_bm25 1.0.0`、`pg_tokenizer 1.0.0` 在全部 **16 个系统/架构平台 × PG14–18** 的干净安装和基础功能检查通过，共 **80 个 PostgreSQL 环境、240 个扩展安装组合**。570 个候选包的 SHA256 与构建会话记录一致。

五个代表环境的核心功能、索引维护、事务、并发、备份与恢复测试完成。**发现两项可复现的 vchord 排序问题，不能给出“所有检查无条件通过”的结论**：vchordg 默认搜索参数下，普通 vector 也可能明显倒序；halfvec 另有微小精度倒序，`vchordrq + cosine` 只需两行就能复现。BM25 与 tokenizer 本轮未发现需要修复的功能缺陷。

本次直接测试已构建的候选二进制包。历史 SQL 只作为升级测试夹具加入一次性容器；当前安装 SQL、control 和共享库保持包内版本，深测结束后的 `rpm -V` / `dpkg --verify` 校验通过。

## P2：vchordg 默认搜索可能返回明显倒序的 vector 结果

复现文件：[bin/qa/vchordg-order.sql](../bin/qa/vchordg-order.sql)。在预加载 vchord 的一次性数据库运行：

```bash
psql -X -v ON_ERROR_STOP=1 -d disposable_qa -f bin/qa/vchordg-order.sql
```

固定 8,000 条 `vector(64)`，使用 `vchordg (v vector_l2_ops)` 和默认搜索参数 `ef_search=64`、`beam_search=1`。查询第 3955 条向量的 top-20，即使不带过滤，也返回以下相邻记录：

```text
id     v <-> query
7126   5.068506892121043
2637   5.009469601695136
```

两条距离相差约 **0.0590**，不是浮点尾数误差。EL10/ARM64/PG18 和 Debian13/x86_64/PG18 均复现，浮点末位略有差异。该查询的 top-20 集合与顺序扫描完全相同，召回率 100%，但返回次序错误；不能把倒序归因于漏召回。

定向测试追加了 **180 次查询对照**：两平台 × L2/IP/cosine × 有/无租户过滤 × 5 个查询 × 3 组搜索参数。默认参数下，EL10 有 21/30、Debian13 有 19/30 次查询发生倒序，IP 最大相邻差约 1.8912。两平台本轮最低单次召回均为：默认参数 75%，2000/2000 为 90%，65535/65535 为 100%。这些数值只描述本次固定数据和新建索引。

在这次定向测试的新建索引上，2000/2000 与 65535/65535 未观察到 vector 倒序；但此前 Debian13 的完整生命周期测试在 2000/2000 已记录带过滤的 vector 倒序。因此不能把调大参数当成严格排序保证。源代码定位入口是 `crates/vchordg/src/search.rs`：搜索迭代器每次返回结果前会继续扩展候选，再从当前集合取最小值，后续发现的候选仍可能小于已经输出的值。尚未修改实现。

[当前图索引文档](https://vchord.pgsty.com/docs/vchord/usage/graph-index/)说明了搜索参数与召回/性能的关系，但未明确说明这种返回次序限制。建议将它作为接口语义问题处理：修正排序保证，或明确说明结果为宽松排序，并在要求严格次序的调用路径显式重排。后文的 MATERIALIZED CTE 方法也适用于 vector；它只保证候选集内部排序。

## P2：halfvec 返回距离可能轻微倒序

复现文件：[bin/qa/vchord-halfvec-order.sql](../bin/qa/vchord-halfvec-order.sql)。在预加载 vchord 的一次性数据库运行：

```bash
psql -X -v ON_ERROR_STOP=1 -d disposable_qa -f bin/qa/vchord-halfvec-order.sql
```

固定的两条 `halfvec(64)` 记录，使用 `vchordrq (h halfvec_cosine_ops)`：

```text
id     h <=> query
6661   0.758565605350707
231    0.7585473951807921
```

较大距离排在较小距离前，差约 **1.82×10⁻⁵**。关闭索引扫描后，顺序为 `231, 6661`。设置 `rerank_in_table=true` 仍返回上述倒序。五个深测环境均复现，x86_64 的末尾浮点位略有差异。

这不是漏召回造成的顺序差异：最小复现只有两条记录，两条都返回。8,000 行测试中，在图搜索参数扩大至 65535/65535 的四个平台，`vchordg` 的 halfvec L2/IP/cosine 仍有近分数倒序，最大约 **1.62×10⁻⁴**；这些扩大搜索的运行未观察到 vector 倒序。最小两行样例中的 vchordg 顺序正确，不能用它替代大数据样例对 vchordg 的观察。此处的微小倒序与上一项图搜索在有限参数下的明显倒序分别记录。

代码中的 halfvec cosine 输入会先在半精度类型内归一化，值得作为定位入口：源码归档的 `src/index/vchordrq/opclass.rs`，`Opfamily::input` 中 `HalfvecCosine` 分支。这里是原因线索，尚未实现或验证上游修复。

对需要严格按原始 SQL 距离排序的应用，可对足够多的 ANN 候选执行显式外层重排：

```sql
WITH candidates AS MATERIALIZED (
    SELECT id, embedding <=> :query::halfvec AS distance
    FROM items
    ORDER BY embedding <=> :query::halfvec
    LIMIT 100
)
SELECT * FROM candidates ORDER BY distance + 0 LIMIT 20;
```

此方法保证已取候选的显示顺序；召回率仍取决于候选数量和检索参数。建议在对严格排序敏感的 halfvec 场景放行前，修正实现或明确要求这一步重排。

## 全平台 sanity

每个平台均从新建的 `pgsty/<platform>:latest` 基础容器开始，安装前确认没有 PostgreSQL server 和三个目标扩展。没有复用构建容器的数据目录、已安装扩展或数据库。ARM64 使用本机原生 Docker，x86_64 使用 m3 原生 Docker；所有联网操作经过 HTTP 代理。

| 实测系统 | x86_64 | aarch64 / arm64 | PG 范围 |
|---|---|---|---|
| Rocky Linux 8.10 | 通过 | 通过 | 14–18 |
| Rocky Linux 9.8 | 通过 | 通过 | 14–18 |
| Rocky Linux 10.2 | 通过 | 通过 | 14–18 |
| Debian 12 bookworm | 通过 | 通过 | 14–18 |
| Debian 13 trixie | 通过 | 通过 | 14–18 |
| Ubuntu 22.04.5 jammy | 通过 | 通过 | 14–18 |
| Ubuntu 24.04.5 noble | 通过 | 通过 | 14–18 |
| Ubuntu 26.04.1 resolute | 通过 | 通过 | 14–18 |

PG 小版本为 14.24、15.19、16.15、17.11、18.6；pgvector 为 0.8.7。具体包修订与镜像 ID 保存在逐平台证据中。

每个 PG 环境执行：

- 安装本批三个主包及其真实依赖，初始化 UTF-8 数据库，共同 preload 三个库。
- 创建 vector、vchord、vchord_bm25、pg_tokenizer，断言版本匹配。
- 对 1,000 条向量分别建立 vchordrq、vchordg 索引，检查执行计划和查询结果数量。
- 使用原生 tsvector 建立 BM25 索引，断言匹配文档数。
- 创建 tokenizer analyzer，断言分词位置，并运行 tokenizer → tsvector → BM25 联动排名。
- 保存包清单、依赖、payload 列表、系统信息、initdb/服务/SQL 日志；逐一复核 80 份 sanity 日志。

## 深测范围与结果

| 环境 | 分支 SQL 回归文件 | tokenizer 多会话测试 | vchord 升级/符号 | 附加验收 |
|---|---:|---:|---|---|
| EL10.2 / ARM64 / PG18.6 | 93 | 29 | 通过 | 向量生命周期、BM25 恢复、并发维护 |
| EL9.8 / x86_64 / PG17.11 | 93 | 29 | 通过 | 向量生命周期、并发维护 |
| Debian 13 / x86_64 / PG18.6 | 93 | 29 | 通过 | 向量生命周期、BM25 恢复、并发维护 |
| Ubuntu 26.04.1 / ARM64 / PG16.15 | 90 | 29 | 通过 | 向量生命周期、并发维护 |
| EL8.10 / x86_64 / PG14.24 | 90 | 29 | 通过 | 最旧 PG 路径、向量生命周期、并发维护 |

总计 **459 个分支 SQL 回归文件运行、145 个 tokenizer Python 集成用例、5 次 tokenizer 独立 preload 测试**完成并通过。PG14/16 按上游条件排除 3 个 PG17+ 文件。日文回归使用官方 Lindera 6.2.0 外部 IPADIC，保留原有预期结果；早期使用 embedded 配置的失败与改用路径配置后的成功日志都保留。

### vchord

分支回归覆盖 vchordrq 与 vchordg、vector/halfvec、rabitq4/rabitq8、L2/IP/cosine、MaxSim 多向量、内部 K-means 与外部构建、过滤与计划、预取/read_stream、分区与部分索引、统计、采样、权限、无效参数/数值边界、VACUUM、REINDEX、扫描取消和事务异常清理。

额外测试使用固定 **8,000 条 64 维向量**，对两种索引 × 两种数据类型 × 三种距离度量的 **12 个组合**，分别执行普通查询和租户过滤查询。每组 5 个固定查询、top-20；顺序扫描由 pgvector 距离算子给出参考答案，索引查询必须在 EXPLAIN 中实际使用目标索引。包括生命周期各阶段，共记录 **900 次查询对照**；另追加前述 180 次图搜索排序对照。

- RQ 使用 32 个聚类、32 probes、epsilon=4。持久性小索引使用默认无聚类结构与空 probes。
- 图索引 `ef_search=beam_search=2000` 在部分样例出现单次 95%、组均值 97% 的召回，未达到最初设定的 98% 组均值测试门槛。这是有损 ANN 的参数表现，未作为损坏或平台故障。
- 扩大图搜索参数至 `65535` 后，EL8/PG14、EL9/PG17、EL10/PG18、Ubuntu26/PG16 的本组查询全部达到 100% 召回。Debian13/PG18 的完整运行保留参数 2000，最低单次 95%、最低组均值 99%。这些是固定小样本的结果，不能外推为生产性能或召回保证。
- 图搜索的明显倒序与 halfvec 的微小倒序分别记录。扩大搜索参数未消除 halfvec 的微小倒序；召回率达标也不代表次序正确。
- 插入/更新/删除/回滚、VACUUM、REINDEX CONCURRENTLY、REPEATABLE READ 旧快照的可见性检查完成。
- 已提交且未主动 checkpoint 的数据经历 `pg_ctl -m immediate` 后恢复：全表向量指纹一致，索引检索完成。
- pg_dump/pg_restore 重建索引后指纹一致；物理 basebackup、流复制、后续写入重放和备库索引查询完成。

另以 4,000 行、8 维表进行真正同时运行的写入、读取、VACUUM、REINDEX CONCURRENTLY。五个平台共 **7,648 个写事务、1,732 对读查询**，两种索引均有效，维护后查询与顺序扫描一致；最终两张表均为 4,021 行。

### vchord_bm25

12 个分支 SQL 文件覆盖评分、完整排序、NULL/空查询、增长段、WAND、过滤、执行计划、参数覆盖、权限、schema、扫描生命周期与 VACUUM。

另在两个 PG18 环境运行分支的 `tests/acceptance.py --recovery`，全部通过：

- 独立 BM25 数学公式与索引/标量结果对照；平均文档长度变化、墓碑和 TID 复用。
- 小候选批次、OFFSET、过滤后的完整性，prepared/generic plan，易变谓词执行次数。
- 长快照下的发布与回收、ANALYZE 锁、实际并行 VACUUM worker、维护权限。
- 80,000 行起步的 WAND buffer-work 与增长段检查；该项是回归门槛，不是正式基准测试。
- 在合并输出、退休页回收期间取消或杀死测试 backend，随后确认 WAL 恢复、孤立页清理和 FSM 稳定。
- 物理备库遇到已回收代际时正确报 40001，墓碑重放不产生错误冲突。

部署边界：分支提供的 `0.3.0 → 1.0.0` 升级 SQL 明确拒绝原地升级。这里的全平台新安装通过，不代表旧版 BM25 数据库可以直接执行 `ALTER EXTENSION UPDATE`；本轮没有演练旧二进制的数据迁移。

### pg_tokenizer

16 个 SQL 文件覆盖内置模型、analyzer、中文 Jieba、日文 Lindera、法/德词干、ngram、停用词、同义词、自定义模型与触发器、原生 tsvector、位置与转义。

每个环境的 29 个集成用例还覆盖相反词序并发写入、批量触发器、锁隔离、强隔离重试、回滚、跨 backend 缓存失效、旧快照、角色与权限、防触发器劫持、两阶段事务限制、prepared plan、并行查询、SQL 0.1.0/0.1.1 → 1.0.0 升级和逻辑备份恢复。独立 preload 测试验证坏条目恢复和不同数据库的同名模型隔离。

包未启用 `lindera-ipadic` 内嵌词典 feature，因此 `embedded://ipadic` 和旧配置 `dictionary.kind="ipadic"` 不适用。官方外部词典路径配置及旧式 `dictionary.path` 均测试通过，包括用户词典。它们是部署条件；不能把未内嵌词典描述为“日文分词全部不可用”。

## 测试夹具修正与验收边界

- 基础镜像不含所有开发测试工具：补装 diffutils/binutils 后重跑升级一致性与符号测试，均通过。
- Rocky 默认 logging_collector 会转移日志。BM25 脚本最初未从指定日志读到并行 worker；仅在其自建测试集群关闭日志转移后，完整恢复验收通过。
- Debian13 x86_64 第一次 apt 安装被容器 8 GB 限额 OOM kill，发生在运行扩展之前；提高到 16 GB 后完成安装和后续测试。其余平台在原限额完成。
- 重跑时遇到已有 standby 路径及续跑脚本辅助函数缺失，均属于夹具问题，保留失败日志并完成后续物理复制校验。
- 没有进行跨 PG 大版本 pg_upgrade、百万/十亿向量性能测试或长时间 soak。SQL 升级测试使用归档中的历史安装脚本和本批库，不等于旧二进制到新二进制的完整数据库迁移演练。

## 证据与复跑材料

证据根目录：`~/.cache/pgext/vchord-qa-20261104/`。

- `package-provenance.json`：全部 570 个包的路径、大小、SHA256，与构建记录核对。
- `qa-summary.json`：五个深测环境的回归数、召回、排序观察、并发计数与备库成功日志；`graph-order-summary.json` 汇总补充的 180 次排序对照。
- `results/<platform>/status.json`、`packages.json`、`setup.log`、`evidence.tar.gz`：镜像 ID、15 个主包、干净安装与各 PG sanity。
- `results/<platform>/server-logs.tar.gz`：补充归档主测试集群的服务日志和配置，包括 logging_collector 写入的数据目录内日志。共复核 110 份日志，未发现 PANIC、SIGSEGV 或 SIGABRT；负向测试产生的预期 SQL 错误与主动故障注入另行保留。
- `results/<platform>/deep-pg<major>/`：逐 SQL 文件结果、集成测试、升级/符号、BM25 恢复、向量查询指标、并发维护及两行复现。EL10a、Debian13 的 `graph-order-metrics.json` 保留追加查询的完整结果、顺序扫描参考和执行计划。
- `scripts/`：本轮执行的 sanity、SQL runner、向量验收和并发维护脚本；`sources/` 是三份已固定版本的源码归档解包副本。
- `bin/ipadic-6.2.0.zip` 与 `lindera-release.json`：官方外部词典及来源记录；`bin/slt-*.tar.gz` 是分支 CI 指定的 sqllogictest 0.29.0。

本轮 16 个 `vcqa1104-*` 测试容器已停止，数据保留供复现；容器 ID 与停止状态记录于 `closure.json`。

候选包来自 RPM `yum/*/vcs1104/` 与 DEB `apt/*/vcs1104/`。本任务的仓库改动为本报告、两份复现 SQL，以及 `.gitignore` 中针对本报告的精确例外；原有 spec、recipe 和构建会话的文档由原任务维护。
